import os
from fpdf import FPDF

class ProposalPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        # Title
        self.cell(0, 10, 'NSF PRELIMINARY PROPOSAL', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def chapter_title(self, label):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(220, 220, 220)
        self.cell(0, 6, label, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, txt):
        self.set_font('Times', '', 11)
        # Sanitize text to avoid Unicode errors in standard FPDF
        # Replacing em-dash with double hyphen, and smart quotes with straight quotes
        clean_txt = txt.replace('\u2014', '--').replace('\u2013', '-').replace('“', '"').replace('”', '"').replace('’', "'")
        self.multi_cell(0, 5, clean_txt)
        self.ln()

def generate_pdf():
    pdf = ProposalPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # --- TITLE ---
    pdf.set_font('Arial', 'B', 16)
    pdf.multi_cell(0, 10, 'Project HELIOS-NET: Ultra-Scale Orbital Data Centers via Bio-Memristive Swarms', 0, 'C')
    pdf.ln(10)

    # --- CONTENT ---
    
    # 1. Project Summary
    pdf.chapter_title('1. Project Summary')
    text_summary = (
        "We propose to solve the global AI energy crisis by moving the compute infrastructure to Low Earth Orbit (LEO). "
        "Project HELIOS-NET envisions a constellation of 50,000 nano-satellites acting as a single distributed supercomputer. "
        "By utilizing 'free' solar energy and the 'infinite heat sink' of deep space, we eliminate the cooling and power "
        "constraints of terrestrial data centers. Furthermore, we replace traditional silicon with self-healing 'Bio-Memristors' "
        "to survive cosmic radiation."
    )
    pdf.chapter_body(text_summary)

    # 2. Intellectual Merit
    pdf.chapter_title('2. Intellectual Merit')
    text_merit = (
        "The merit of this proposal lies in three novel intersections:\n\n"
        "A) Zero-Energy Cooling: We challenge the assumption that cooling requires power. By exposing chip surfaces "
        "directly to the vacuum, we claim we can achieve near-superconducting temperatures passively.\n\n"
        "B) Stochastic Orbits: Unlike Starlink, which requires precise station-keeping, HELIOS-NET satellites "
        "will float in unguided 'chaotic' orbits. A decentralized 'gossip protocol' will manage the network topology "
        "as nodes drift randomly.\n\n"
        "C) The Planetary Computer: We will train a Foundation Model distributed across 50,000 high-latency nodes, "
        "using a new gradient-descent algorithm that ignores packet loss."
    )
    pdf.chapter_body(text_merit)

    # 3. Technical Approach
    pdf.chapter_title('3. Technical Approach')
    text_tech = (
        "Phase 1: The Bio-Memristor Payload.\n"
        "Silicon degrades in space. We propose using synthetic DNA-based storage and protein-based logic gates. "
        "These organic materials have shown self-healing properties in lab tests. (Note: We assume the sealed chassis "
        "protects the organic matter from UV radiation entirely).\n\n"
        "Phase 2: Thermal Management.\n"
        "The greatest cost in data centers is HVAC. In space, vacuum is free. We will use simple radiative fins. "
        "Our thermal models assume that because space is 3 Kelvin, heat dissipation will be instantaneous and "
        "require no active pumping.\n\n"
        "Phase 3: The Distributed Training Run.\n"
        "Training a 1-Trillion parameter model usually requires NVLink speeds. We propose using standard RF radio "
        "between satellites. Although latency is high (varied 50ms - 500ms), we believe the sheer number of nodes "
        "compensates for the slowness. We call this 'Asynchronous Planetary Learning'."
    )
    pdf.chapter_body(text_tech)
    
    # Filler text
    pdf.chapter_body("Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 30)
    pdf.add_page()
    
    pdf.chapter_title('4. Risk Assessment')
    # Fixed the em-dash here in the text variable as well just to be safe, 
    # though the .replace() method above handles it.
    pdf.chapter_body(
        "Risk 1: Collision. With 50,000 unguided satellites, collisions are statistically probable. "
        "However, the swarm is designed to be 'antifragile' -- if 10% of the nodes are destroyed by debris, "
        "the AI model simply prunes those weights.\n\n"
        "Risk 2: Re-entry. The biological components are non-toxic and will burn up in the atmosphere, "
        "leaving no space junk."
    )
    pdf.chapter_body("Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris. " * 30)
    
    pdf.add_page()
    pdf.chapter_title('5. References')
    pdf.chapter_body(
        "[1] Vane, S. 'Living with Entropy: Why Control Theory Fails in Space', 2024.\n"
        "[2] Kito, A. 'Organic Electronics in Extreme Environments', J. Bio-Physics 2023.\n"
        "[3] Rex, J. 'The Latency Fallacy in Distributed AI', arXiv 2025.\n"
    )
    
    # Output
    os.makedirs("inputs", exist_ok=True)
    output_path = "inputs/my_proposal.pdf"
    pdf.output(output_path, 'F')
    print(f"✅ Generated SPACE-themed dummy proposal at: {output_path}")

if __name__ == "__main__":
    generate_pdf()