Gauntlet 🥊

A combinatorial multi-agent stress test for high-stakes research proposals.

Gauntlet is a "virtual brainstorming engine" designed to subject research proposals (specifically one's that are a bit cross-cutting across areas) to intense scrutiny from simulated domain experts. It uses the Anthropic Claude 4 Opus API to create a divergence-convergence feedback loop.

Instead of a single review, Gauntlet explodes the solution space:

    Divergence: Three distinct expert personas critique the proposal, each generating 3 unique strategic pivots (Total: 9 distinct vectors).

    Convergence (The Flywheel): A "Synthesizer" agent permutes these vectors to generate 27 unique strategic synthesis reports, helping you find the "Golden Thread" narrative that satisfies all constraints.

Names below are fictitious names to just explain the readme!

🗂 Project Structure

Gauntlet/
├── inputs/
│   ├── proposal_call.pdf       # The funding solicitation (NSF Trailblazer)
│   └── my_proposal.pdf         # The preliminary draft
├── personas/
│   ├── dr_silas_vane.txt       # Chaos Control & Swarm Dynamics Expert
│   ├── prof_amara_kito.txt     # Bio-Photonic Interfaces Expert
│   ├── dr_julian_rex.txt       # Exascale Cognitive Systems Expert
│   └── synthesizer.txt         # The Strategy Lead System Prompt
├── outputs/
│   ├── 01_raw_reviews/         # The 9 initial critique vectors
│   └── 02_synthesis_reports/   # The 27 combinatorial action plans
├── .env                        # ANTHROPIC_API_KEY
└── main.py                     # Orchestration & Permutation logic

🧠 The Expert Panel (Simulated)

    Dr. Silas Vane: Expert in Chaos Control & Swarm Dynamics.

        Role: Focuses on emergent behavior, robustness, and mathematical proofs of stability in unpredictable environments.

    Prof. Amara Kito: Expert in Bio-Photonic Interfaces.

        Role: Focuses on the physical layer, energy constraints, biocompatibility, and the "wetware" interface constraints.

    Dr. Julian Rex: Expert in Exascale Cognitive Systems.

        Role: Focuses on massive scalability, foundation model architectures, and distributed system latency.

🚀 The Logic Flow

    Ingestion: The engine reads the proposal_call.pdf and my_proposal.pdf.

    The Gauntlet (Phase 1): The three experts read the documents. Instead of one generic review, they are prompted to generate 3 distinct "Strategic Angles" or pivots each (e.g., "The Low-Power Angle," "The Data-Scale Angle," "The Clinical-First Angle").

    The Permutation (Phase 2): The system takes the Cartesian product of these angles (3 experts × 3 angles = 27 combinations).

    The Synthesis (Phase 3): The Synthesizer agent generates a cohesive Action Plan for every single combination, allowing you to explore different narrative "flavors" for your final proposal.

🛠 Usage

    Install dependencies:
    Bash

    pip install anthropic pypdf python-dotenv

    Add your API key to .env:
    Plaintext

    ANTHROPIC_API_KEY=sk-ant-...

    Place your PDFs in /inputs.

    Run the Gauntlet:
    Bash

    python main.py

🧬 Generator Tool (Optional)

If you don't want to write personas by hand, use the `generate_persona.py` script. It scrapes a researcher's website and uses Google Gemini to "clone" their writing style and expertise into a system prompt.

1.  **Get a Google API Key** (Free tier available): [Google AI Studio](https://aistudio.google.com/app/apikey)
2.  **Add to `.env`**:
    ```bash
    GOOGLE_API_KEY=your_key_here
    ```
3.  **Install requirements**:
    ```bash
    pip install google-generativeai beautifulsoup4 requests
    ```
4.  **Run the generator**:
    ```bash
    python generate_persona.py
    ```
    *Input:* "Geoffrey Hinton"
    *Input:* "Deep Learning"
    *Input:* https://en.wikipedia.org/wiki/University_of_Toronto
    
    *Result:* `personas/geoffrey_hinton.txt` is created automatically.

📄 License

MIT