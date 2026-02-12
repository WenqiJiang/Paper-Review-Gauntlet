import os
import sys
import argparse
import json
import requests
from bs4 import BeautifulSoup
from anthropic import Anthropic
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Configure the Anthropic API (same key used for Gauntlet reviews)
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
if not ANTHROPIC_API_KEY:
    print("\n❌ ANTHROPIC_API_KEY not found in .env file")
    print("Add your API key to .env:")
    print("  echo 'ANTHROPIC_API_KEY=sk-ant-...' >> .env")
    sys.exit(1)

client = Anthropic(api_key=ANTHROPIC_API_KEY)

def scrape_bio_data(url):
    """
    Fetches and cleans text content from a URL to use as context for the persona.
    """
    print(f"🕵️  Scraping context from: {url}...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Strip out script and style elements
        for script in soup(["script", "style", "nav", "footer"]):
            script.decompose()
            
        text = soup.get_text(separator=' ')
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        # Truncate if massively long (Gemini has a huge context, but let's be safe)
        return text[:20000] 
        
    except Exception as e:
        print(f"⚠️  Could not scrape URL: {e}")
        return None

def generate_system_prompt(name, expertise, bio_text):
    """
    Uses Claude to craft a high-fidelity system prompt based on the scraped data.
    """
    print(f"🧠  Generating persona for {name} using Claude...")

    meta_prompt = f"""You are an expert Prompt Engineer specializing in "Roleplay Personas" for advanced AI agents.

**Goal:** Write a system prompt for an AI agent to roleplay as {name}, a world-class expert in {expertise}.

**Context Material (Bio/Papers):**
{bio_text}

**Instructions:**
1. Create a deep psychological profile based on the bio. What do they value? (e.g., efficiency, clinical outcomes, mathematical purity).
2. Define their "Voice": specific jargon, tone (skeptical, visionary, pragmatic), and critique style.
3. Define their "Mission": They are reviewing a high-stakes research proposal or paper. They need to find holes in it and provide constructive criticism.
4. Define their reviewing priorities: What aspects do they scrutinize most carefully? What are their "pet peeves"?

**Output Format:**
Return ONLY the system prompt text. Do not include introductory text like "Here is the prompt."
Start the output with: "**System Prompt:** You are {name}..."

The persona should be detailed, capturing their unique perspective and expertise."""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",  # Latest Sonnet, excellent for persona generation
        max_tokens=4096,
        messages=[
            {"role": "user", "content": meta_prompt}
        ]
    )

    return response.content[0].text

def generate_single_persona(name, expertise, url):
    """Generate a single persona."""
    print(f"\n📝 Generating persona for: {name}")

    # Scrape
    bio_text = scrape_bio_data(url) if url else None
    if not bio_text:
        bio_text = "No bio provided. Please infer based on general knowledge of this person."

    # Generate
    persona_text = generate_system_prompt(name, expertise, bio_text)

    # Save
    filename = f"personas/{name.lower().replace(' ', '_')}.md"
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w", encoding='utf-8') as f:
        f.write(persona_text)

    print(f"✅  Persona saved to: {filename}")
    return filename

def load_personas_from_config(config_path):
    """Load persona specifications from a JSON config file."""
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config.get('personas', [])

def main():
    parser = argparse.ArgumentParser(
        description="Generate expert reviewer personas for Gauntlet",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (prompt for each persona)
  python generate_persona.py

  # Batch mode from config file
  python generate_persona.py -c persona_config.json

  # Single persona with args
  python generate_persona.py -n "Gustavo Alonso" -e "Database Systems" -u "https://people.inf.ethz.ch/alonso/"

Config file format (persona_config.json):
{
  "personas": [
    {
      "name": "Gustavo Alonso",
      "expertise": "Database Systems, Distributed Systems",
      "url": "https://people.inf.ethz.ch/alonso/"
    },
    {
      "name": "Torsten Hoefler",
      "expertise": "High-Performance Computing, Parallel Computing",
      "url": "https://htor.inf.ethz.ch/"
    },
    {
      "name": "Christos Kozyrakis",
      "expertise": "Datacenters, Cloud Computing",
      "url": "https://web.stanford.edu/~kozyraki/"
    }
  ]
}
        """
    )
    parser.add_argument('-c', '--config', type=str,
                        help='Path to JSON config file with persona specifications')
    parser.add_argument('-n', '--name', type=str,
                        help='Expert name (for single persona generation)')
    parser.add_argument('-e', '--expertise', type=str,
                        help='Area of expertise (for single persona generation)')
    parser.add_argument('-u', '--url', type=str,
                        help='URL for bio/wiki/lab page (for single persona generation)')

    args = parser.parse_args()

    print("--- 🧬 Gauntlet Persona Generator 🧬 ---\n")

    # Mode 1: Config file (batch mode)
    if args.config:
        print(f"📂 Loading personas from: {args.config}")
        personas = load_personas_from_config(args.config)
        print(f"Found {len(personas)} persona(s) to generate\n")

        for i, persona_spec in enumerate(personas, 1):
            print(f"[{i}/{len(personas)}]", end=" ")
            name = persona_spec.get('name')
            expertise = persona_spec.get('expertise')
            url = persona_spec.get('url', '')

            if not name or not expertise:
                print(f"⚠️  Skipping invalid entry: {persona_spec}")
                continue

            generate_single_persona(name, expertise, url)

        print(f"\n🎉 Generated {len(personas)} personas successfully!")

    # Mode 2: Single persona with command-line args
    elif args.name and args.expertise:
        generate_single_persona(args.name, args.expertise, args.url or '')

    # Mode 3: Interactive mode (legacy)
    else:
        print("Interactive Mode")
        print("(Tip: Use -c config.json for batch generation)\n")

        name = input("Enter Expert Name (e.g., Gustavo Alonso): ")
        expertise = input("Enter Area of Expertise (e.g., Database Systems): ")
        url = input("Enter URL for Bio/Wiki/Lab Page (optional): ")

        generate_single_persona(name, expertise, url)

    print("\n------------------------------------------")
    print("Done! Personas are in the personas/ directory")

if __name__ == "__main__":
    main()