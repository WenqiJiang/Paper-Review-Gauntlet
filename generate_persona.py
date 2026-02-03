import os
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Google API
# Get your key here: https://aistudio.google.com/app/apikey
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("Please set GOOGLE_API_KEY in your .env file")

genai.configure(api_key=GOOGLE_API_KEY)

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
    Uses Gemini to craft a high-fidelity system prompt based on the scraped data.
    """
    print(f"🧠  Generating persona for {name} using Gemini...")
    
    model = genai.GenerativeModel('gemini-2.5-pro')
    
    meta_prompt = f"""
    You are an expert Prompt Engineer specializing in "Roleplay Personas" for advanced AI agents.
    
    **Goal:** Write a system prompt for an AI agent to roleplay as {name}, a world-class expert in {expertise}.
    
    **Context Material (Bio/Papers):**
    {bio_text}
    
    **Instructions:**
    1. Create a deep psychological profile based on the bio. What do they value? (e.g., efficiency, clinical outcomes, mathematical purity).
    2. Define their "Voice": specific jargon, tone (skeptical, visionary, pragmatic), and critique style.
    3. Define their "Mission": They are reviewing a high-stakes research proposal (NSF Proposal call name). They need to find holes in it.
    4. Define a specific "Collaboration Angle": How would they propose joining the project?
    
    **Output Format:**
    Return ONLY the system prompt text. Do not include introductory text like "Here is the prompt."
    Start the output with: "**System Prompt:** You are {name}..."
    """
    
    response = model.generate_content(meta_prompt)
    return response.text

def main():
    print("--- 🧬 Gauntlet Persona Generator 🧬 ---")
    
    # User Inputs
    name = input("Enter Expert Name (e.g., Ada Lovelace): ")
    expertise = input("Enter Area of Expertise (e.g., Early Computing): ")
    url = input("Enter URL for Bio/Wiki/Lab Page: ")
    
    # Scrape
    bio_text = scrape_bio_data(url)
    if not bio_text:
        bio_text = "No bio provided. Please infer based on general knowledge of this person."
    
    # Generate
    persona_text = generate_system_prompt(name, expertise, bio_text)
    
    # Save
    filename = f"personas/{name.lower().replace(' ', '_')}.md"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, "w", encoding='utf-8') as f:
        f.write(persona_text)
        
    print(f"\n✅  Persona saved to: {filename}")
    print("------------------------------------------")
    print(persona_text[:500] + "...\n")

if __name__ == "__main__":
    main()