# Gauntlet 🥊

**Multi-Agent Critique Engine for Research Papers and Proposals**

Gauntlet uses AI to simulate a panel of expert reviewers who critique your work from multiple perspectives. Instead of getting a single review, you get comprehensive feedback that helps you identify weaknesses before submission, strengthen your arguments, and find the narrative that satisfies diverse expert viewpoints.

## What Does It Do?

Gauntlet takes your document (paper draft, proposal, or idea) and:

1. **Divergence Phase**: Runs it through multiple expert personas, each reviewing at different "temperatures" (conservative, balanced, creative) to generate diverse critiques
2. **Convergence Phase**: A "Synthesizer" agent analyzes all combinations of reviews and produces strategic synthesis reports that help you find the strongest path forward

Think of it as a **virtual committee meeting** where experts debate your work from their specialized angles, and a strategy lead distills their conflicting advice into actionable recommendations.

## Use Cases

- 📝 **Pre-Submission Paper Review**: Get tough feedback on your paper draft before sending it to a conference
- 💡 **Proposal Development**: Stress-test research proposals against diverse expert criteria
- 📖 **Deep Paper Analysis**: Understand complex papers through multi-perspective deconstruction
- 🧪 **Idea Incubation**: Develop and refine early-stage research ideas

---

## Quick Start

### 1. Installation

```bash
pip install anthropic pypdf python-dotenv
```

### 2. Setup

Create a `.env` file with your API key:

```bash
ANTHROPIC_API_KEY=sk-ant-...
```

### 3. Run

**For paper criticism (most common use case):**

```bash
# Basic run with existing personas
python main.py inputs/placeholder.pdf inputs/your_paper.pdf

# Or with a custom config
python main.py inputs/placeholder.pdf inputs/your_paper.pdf -c config_archresearch.toml
```

**For proposal review:**

```bash
python main.py inputs/call_for_proposals.pdf inputs/your_proposal.pdf
```

### 4. Review Results

Check the `outputs/` directory:
- `expert_reviews/` - Individual critiques from each expert
- `syntheses/` - Combined analysis folders with `SYNTHESIS.md` files

---

## 🔍 How It Works

### Phase 1: Divergent Expert Reviews

Each expert persona reviews your document at multiple "temperatures":
- **Temperature 0.3**: Conservative, precise, risk-averse critique
- **Temperature 0.7**: Balanced perspective
- **Temperature 1.0**: Creative, bold, divergent thinking

**Example**: With 3 experts × 3 temperatures = 9 distinct reviews

### Phase 2: Convergent Synthesis

A "Synthesizer" agent reads all combinations of reviews (one per expert) and produces strategic synthesis reports:
- 3 experts with 3 reviews each = 3³ = 27 unique synthesis reports
- Each synthesis folder is self-contained with the full source reviews included

### Why This Approach?

- **No blind spots**: Different temperature settings naturally explore conservative vs. bold critiques
- **Cross-perspective insights**: Synthesis reports identify common themes and conflicting advice
- **Exhaustive coverage**: Combinatorial approach ensures you see how different expert viewpoints interact
- **Idempotent**: If interrupted (e.g., rate limits), re-run safely—completed outputs are skipped

---

## 📝 Using Gauntlet to Criticize Your Paper Before Submission

This is one of the most powerful use cases. Here's a complete workflow:

### Step 1: Choose or Generate Expert Personas

You need reviewers who represent the perspectives your paper will face at the target conference/journal.

#### Option A: Use Existing Personas

Check the `personas/` directory for pre-built experts:

```bash
ls personas/
```

Example personas include experts in microarchitecture, workload analysis, simulation tools, quantum computing, etc.

#### Option B: Generate Custom Personas (Recommended)

Create personas that match your paper's domain and target venue's typical reviewers:

```bash
# Install additional requirements
pip install google-generativeai beautifulsoup4 requests

# Add Google API key to .env (free tier at https://aistudio.google.com/app/apikey)
echo "GOOGLE_API_KEY=your_key_here" >> .env

# Run the generator
python generate_persona.py
```

**Interactive prompts:**
- **Researcher name**: "Onur Mutlu" (or any expert name)
- **Research area**: "Computer Architecture, Memory Systems"
- **URL** (optional): "https://people.inf.ethz.ch/omutlu/"

The script creates `personas/onur_mutlu.md` automatically.

**Pro tip for paper reviews**: Generate 3-4 personas representing:
1. **Methodology critic** - Focuses on experimental rigor, baselines, statistical significance
2. **Theory/systems expert** - Checks technical soundness, proofs, assumptions
3. **Practitioner** - Evaluates real-world applicability, limitations, reproducibility
4. **Senior generalist** - Assesses positioning, novelty, writing clarity, contribution claims

### Step 2: Create a Custom Config File

Create `config_paperreview.toml` in the project root:

```toml
# Synthesizer persona (combines all reviews into actionable advice)
synthesizer = "synthesizer_paper_analyst"

# Expert-reviewer personas (add 3-4 for comprehensive coverage)
[[personas]]
name  = "onur_mutlu"
short = "mutlu"

[[personas]]
name  = "prof_methodology_expert"
short = "method"

[[personas]]
name  = "dr_practitioner"
short = "practice"

[[personas]]
name  = "senior_generalist"
short = "senior"
```

**Notes:**
- `name` should match the filename in `personas/` (without `.md`)
- `short` is used in output folder names
- Order matters: it defines the combination naming in synthesis folders

### Step 3: Customize the Synthesizer (Important!)

The synthesizer determines what kind of advice you get. Edit or create a synthesizer persona:

**For paper reviews**, use or edit `personas/synthesizer_paper_analyst.md`:

```markdown
**System Prompt:**
You are a Senior Review Strategist for [Your Target Conference, e.g., ISCA/MICRO].
You've just received reviews from a panel of expert reviewers on a paper draft.

**Your Goal:**
Synthesize the reviews into a prioritized action plan for revision that addresses:
1. **Fatal flaws** that would cause rejection (missing baselines, unsupported claims, unfair comparisons)
2. **Major concerns** that need new experiments or significant rewrites
3. **Minor issues** for clarity and polish
4. **Positioning** - How to better frame the contribution for [Conference] audience

**Output Structure:**
1. **Rejection Risk Assessment** (High/Medium/Low)
2. **Critical Issues** (Must fix before submission)
3. **Recommended Additions** (Experiments, comparisons, analysis)
4. **Framing Improvements** (Abstract, introduction, contribution claims)
5. **Specific Rewrite Directives** by section

**Tone:** Direct, actionable, prioritized by impact on acceptance probability.
```

### Step 4: Run the Critique

```bash
python main.py inputs/placeholder.pdf inputs/your_paper_draft.pdf -c config_paperreview.toml -o outputs/paper_review_jan2026
```

**Arguments explained:**
- **First PDF**: A placeholder document (can be any PDF, or create a simple one describing the conference CFP)
- **Second PDF**: Your paper draft
- **`-c config_paperreview.toml`**: Your custom configuration
- **`-o outputs/paper_review_jan2026`**: Output directory (optional, defaults to `outputs/`)

**Note on placeholder PDF**: For paper reviews, the first PDF isn't critical. You can create a simple one-page PDF that says "Conference: ISCA 2026, Focus: Computer Architecture" or just use any PDF as a placeholder.

### Step 5: Adjust Temperature Settings (Optional)

By default, `main.py` runs at temperature 0.3 only (1 review per expert for speed).

To get the full divergent experience with multiple perspectives per expert:

**Edit `main.py` around line 51:**

```python
# OPTION 1: Fast mode (1 review per expert - CURRENT DEFAULT)
TEMPERATURES: list[float] = [0.3]

# OPTION 2: Full divergence (3 reviews per expert - UNCOMMENT THIS)
# TEMPERATURES: list[float] = [0.3, 0.7, 1.0]
```

**Trade-off:**
- **Fast mode** (temp 0.3 only): 4 experts = 4 reviews + 4 syntheses (~$5-10, 10-15 min)
- **Full mode** (3 temps): 4 experts = 12 reviews + 81 syntheses (~$50-80, 1-2 hours)

For paper criticism, **full mode is recommended** if budget allows—you get conservative, balanced, and creative critiques from each expert.

### Step 6: Analyze the Results

After the run completes, check your output directory:

```
outputs/paper_review_jan2026/
├── RUN_CONFIG.md                    # Metadata about this run
├── expert_reviews/                  # Individual reviews
│   ├── onur_mutlu/
│   │   ├── run_1.md                # Conservative (temp 0.3)
│   │   ├── run_2.md                # Balanced (temp 0.7)
│   │   └── run_3.md                # Creative (temp 1.0)
│   ├── prof_methodology_expert/
│   │   └── ...
│   └── ...
└── syntheses/                       # Combined analyses
    ├── mutlu_1__method_1__practice_1__senior_1/
    │   ├── SYNTHESIS.md            # ← START HERE
    │   ├── onur_mutlu_review.md
    │   ├── prof_methodology_expert_review.md
    │   ├── dr_practitioner_review.md
    │   └── senior_generalist_review.md
    └── ...                          # More synthesis combinations
```

#### Reading Strategy

1. **Start with 2-3 synthesis reports** from different temperature combinations:
   - `mutlu_1__method_1__practice_1__senior_1/` (all conservative)
   - `mutlu_2__method_2__practice_2__senior_2/` (all balanced)
   - `mutlu_3__method_3__practice_3__senior_3/` (all creative)

2. **Identify recurring themes**:
   - What issues appear in *all* synthesis reports? → High priority fixes
   - What suggestions only appear at higher temps? → More speculative improvements

3. **Deep dive into individual reviews** for specific concerns:
   - Read the full expert reviews copied into each synthesis folder
   - Look for concrete suggestions (e.g., "compare against X", "clarify assumption Y")

4. **Create a revision checklist**:
   ```markdown
   ## Critical (Must fix for submission)
   - [ ] Add missing baseline comparison to [X]
   - [ ] Fix overclaimed speedup in abstract (say "up to 2.3x" not "10x")

   ## Major (Significantly improves chances)
   - [ ] Run sensitivity analysis for parameter Y
   - [ ] Expand related work section covering [recent paper]

   ## Minor (Polish)
   - [ ] Improve Figure 3 clarity
   - [ ] Rewrite intro paragraph 2 for better flow
   ```

### Step 7: Iterate

After revising your paper based on feedback:

```bash
# Run again on the revised draft
python main.py inputs/placeholder.pdf inputs/revised_paper_v2.pdf -c config_paperreview.toml -o outputs/paper_review_feb2026
```

Compare the new synthesis reports with the old ones:
- Were the critical issues addressed?
- Do new concerns appear?
- Has the "rejection risk" assessment improved?

---

## 🧬 Persona Generator Details

The `generate_persona.py` script is powerful for creating realistic expert reviewers. Here's what it does:

### How It Works

1. **Web scraping**: Fetches content from the provided URL (researcher homepage, lab page, etc.)
2. **Content extraction**: Pulls research interests, paper titles, project descriptions
3. **Persona generation**: Uses Google Gemini to create a review persona that captures:
   - Research focus and expertise areas
   - Reviewing style and priorities
   - Common questions/concerns they'd raise
   - Tone and perspective

### Tips for Good Personas

**For paper criticism:**
- Use researchers who publish in your target venue
- Include people with different perspectives (theorist vs. practitioner vs. tool-builder)
- Mix seniority levels (1-2 senior PIs, 1-2 rising stars)

**For proposal reviews:**
- Model personas after likely program committee members
- Include domain experts AND interdisciplinary reviewers
- Add a "skeptical engineer" who questions feasibility

**URL sources that work well:**
- Personal academic homepages (best)
- University faculty pages
- Google Scholar profiles
- Lab/group websites
- Wikipedia pages for well-known researchers

**Example persona generation workflow:**

```bash
python generate_persona.py
# Input: "Onur Mutlu"
# Input: "Computer Architecture, Memory Systems, Hardware Security"
# Input: https://people.inf.ethz.ch/omutlu/

python generate_persona.py
# Input: "Christos Kozyrakis"
# Input: "Datacenters, Cloud Computing, Computer Architecture"
# Input: https://web.stanford.edu/~kozyraki/

python generate_persona.py
# Input: "Margaret Martonosi"
# Input: "Mobile Computing, Sustainability, Computer Architecture"
# Input: https://www.cs.princeton.edu/~mrm/
```

This gives you three diverse architecture researchers with different focuses.

---

## 🎛️ Advanced: Tuning the Synthesizer

The synthesizer is your strategic advisor. Different use cases need different synthesizer goals:

### For Paper Reviews

**Goal**: Identify weaknesses before submission

```markdown
**Your Goal:**
You are preparing this paper for [Conference] submission. Prioritize:
1. Fatal flaws (would cause desk reject or strong reject)
2. Missing experiments that weaken claims
3. Positioning issues (underselling or overclaiming)
4. Comparison fairness and baseline selection
```

### For Grant Proposals

**Goal**: Find the "golden thread" narrative

```markdown
**Your Goal:**
You are a grant strategy consultant. The experts have conflicting advice.
Find the unifying narrative that:
1. Satisfies all expert concerns simultaneously
2. Aligns with the funding agency's priorities
3. Differentiates from existing funded projects
4. Presents a credible team and plan
```

### For Paper Reading/Learning

**Goal**: Teach understanding

```markdown
**Your Goal:**
You are a PhD advisor helping a student understand this paper.
Synthesize the expert analyses to:
1. Explain the core contribution simply
2. Clarify the "trick" that makes it work
3. Contextualize it in the research landscape
4. Identify limitations and open questions
```

Edit the appropriate synthesizer persona file in `personas/` to match your needs.

---

## 💡 Advanced: Idea Generation (Optional Front-End)

Before running critiques, you can use `idea_generator.py` to develop ideas that already anticipate expert objections.

### What It Does

Takes a rough idea and baseline paper, then generates a proposal that's been written *against* your expert personas—anticipating their concerns before they review it.

### Usage

```bash
# Install additional dependency for PDF generation
pip install markdown-pdf

# Run the generator
python idea_generator.py
```

You'll be prompted for:
- Baseline paper (PDF)
- Rough idea description
- Which personas to design against

**Output:**
- Markdown draft in `outputs/idea_generation/`
- Auto-generated PDF ready for Gauntlet review

See [IDEAGEN.md](IDEAGEN.md) for the full concept and detailed instructions.

---

## 🗂️ Project Structure

```
Gauntlet/
├── inputs/
│   └── your_paper.pdf              # Your document to review
├── personas/
│   ├── *.md                        # Expert reviewer personas
│   ├── synthesizer*.md             # Strategy synthesizer personas
│   └── template_*.md               # Templates for creating new personas
├── outputs/
│   ├── RUN_CONFIG.md               # Run metadata
│   ├── expert_reviews/             # Individual reviews (N personas × M temps)
│   │   └── persona_name/
│   │       ├── run_1.md           # Temperature 0.3
│   │       ├── run_2.md           # Temperature 0.7
│   │       └── run_3.md           # Temperature 1.0
│   └── syntheses/                  # All combination syntheses
│       └── persona1_X__persona2_Y__persona3_Z/
│           ├── SYNTHESIS.md       # Combined strategic analysis
│           └── *_review.md        # Copies of source reviews
├── config*.toml                    # Configuration files for different modes
├── main.py                         # Main orchestration script
├── generate_persona.py             # Persona generator tool
├── idea_generator.py               # Optional idea generation front-end
├── .env                            # API keys (ANTHROPIC_API_KEY, GOOGLE_API_KEY)
└── README.md                       # This file
```

---

## 📖 Other Modes

### Paper Reading Mode

Use Gauntlet to deeply understand a published paper by having experts "deconstruct" it:

```bash
python main.py inputs/placeholder.pdf inputs/paper_to_analyze.pdf -c config_readpaper_archgeneric.toml
```

The reviewers will explain:
- The core contribution vs. marketing fluff
- The "magic trick" mechanism that makes it work
- Strengths and weaknesses in the evaluation
- How it fits in the research landscape

### Proposal Development Mode

Stress-test research proposals against funding agency criteria:

```bash
python main.py inputs/nsf_solicitation.pdf inputs/my_proposal.pdf -c config_base.toml
```

Experts critique from different angles (technical feasibility, broader impact, team qualifications), and the synthesizer finds the "golden thread" narrative that satisfies all requirements.

---

## ⚙️ Configuration Files

Gauntlet uses TOML config files to specify personas and settings:

**`config_base.toml`**: Default configuration for proposal reviews
**`config_archresearch.toml`**: Computer architecture research focus
**`config_readpaper_archgeneric.toml`**: Generic paper reading/analysis mode

**Create your own:**

```toml
# config_mypaperreview.toml

synthesizer = "synthesizer_paper_analyst"

[[personas]]
name  = "expert_1"
short = "e1"

[[personas]]
name  = "expert_2"
short = "e2"

# Add more personas as needed
```

---

## 🔧 Troubleshooting

### Rate Limits

If you hit API rate limits mid-run:
1. Just wait a few minutes
2. Re-run the exact same command
3. The script is **idempotent**—it skips completed outputs and resumes

### Cost Management

**Typical costs (with Claude Opus 4.5):**
- **Fast mode** (temp 0.3, 4 experts): ~$5-10, 10-15 minutes
- **Full mode** (3 temps, 4 experts): ~$50-80, 1-2 hours

**Tips:**
- Start with fast mode to test your personas
- Use full mode for final pre-submission review
- Limit to 3-4 personas for most use cases

### Persona Quality

If reviews feel generic:
- Add more specific details to persona prompts (recent papers, pet peeves)
- Use the persona generator with detailed URLs
- Edit generated personas to emphasize specific reviewing priorities

### Synthesis Overload

If you get too many synthesis reports (e.g., 81 with 4 experts × 3 temps):
- Start with the "corner" cases: all-conservative, all-balanced, all-creative
- Look for patterns across ~5 synthesis reports rather than reading all
- Focus on synthesis reports that combine diverse temperatures (e.g., conservative + creative)

---

## 📄 License

MIT

---

## 🙏 Acknowledgments

Gauntlet uses:
- **Anthropic Claude Opus 4.5** for expert review generation
- **Google Gemini** (optional) for persona generation
- Inspired by the need for pre-submission stress-testing in high-stakes research

---

## 📚 Additional Resources

- **[IDEAGEN.md](IDEAGEN.md)**: Deep dive into the idea generation front-end
- **[TOPICS.txt](TOPICS.txt)**: List of research areas with pre-defined persona categories
- **`examples/`**: Example configurations and output structures for different modes
  - `examples/incubator_mode/`: Early-stage idea development
  - `examples/paper_reader_mode/`: Published paper analysis

---

**Questions or issues?** Check the scripts' docstrings or open an issue on the repository.
