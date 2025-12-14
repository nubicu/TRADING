import { useState } from 'react';
import { Container, Nav, Navbar, Table, Row, Col, Image } from 'react-bootstrap';
import robyHeadshot from './assets/Roby_head.jpg';

function App() {
  const [isNavExpanded, setIsNavExpanded] = useState(false);

  return (
    <>
      <Navbar
        bg="dark"
        variant="dark"
        expand="lg"
        sticky="top"
        expanded={isNavExpanded}
        onToggle={setIsNavExpanded}
      >
        <Container>
          <Navbar.Brand href="#home">Buzabrici-Filipescu Robert</Navbar.Brand>
          <Navbar.Toggle
            aria-controls="basic-navbar-nav"
            onClick={() => setIsNavExpanded(!isNavExpanded)}
            className="custom-toggle"
          >
            {isNavExpanded ? (
              <div className="close-icon">
                <span></span>
                <span></span>
              </div>
            ) : (
              <div className="hamburger-icon">
                <span></span>
                <span></span>
                <span></span>
              </div>
            )}
          </Navbar.Toggle>
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto">
              <Nav.Link href="#about">About</Nav.Link>
              <Nav.Link href="#experience">Experience</Nav.Link>
              <Nav.Link href="#education">Education</Nav.Link>
              <Nav.Link href="#projects">Projects</Nav.Link>
              <Nav.Link href="#skills">Skills</Nav.Link>
              <Nav.Link href="#languages">Languages</Nav.Link>
              <Nav.Link href="#contact">Contact</Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>

      <main>
        <section id="about" className="py-3 bg-section-1">
          <Container>
            <h2>About Me</h2>
            <Row>
              <Col md={8}>
                <p>Senior Embedded Software Engineer with over 13 years of experience in automotive and space-grade systems, specializing in instrument cluster development, CAN communication and AUTOSAR-based systems. Proven track record of delivering robust and high-performance embedded solutions for OEMs including Daimler, Ford, Renault, Volkswagen, Porsche, and Audi.</p>
                <ul>
                  <li>Reduced debugging time by 25% through rigorous code reviews and adherence to coding standards.</li>
                  <li>Enhanced code reliability by 25% via comprehensive unit and component testing strategies.</li>
                  <li>Delivered over 300 code commits, ensuring consistent quality and timely releases.</li>
                  <li>Created a centralized knowledge base of 50+ software modules, reducing integration errors by 20% and improving cross-team collaboration.</li>
                </ul>
                <p>Skilled in ANSI C, CANoe, Trace32, and Google Test, with hands-on experience in V-Cycle and Agile development, diagnostics and calibration protocols (CCP, XCP), and ISO 26262 compliance. Currently focused on expanding expertise in modern programming languages including C++, C#, Python, and Rust to drive innovation in embedded systems.</p>
                <p>Seeking opportunities in collaborative environments that value technical excellence, mentorship, and continuous improvement.</p>
                <h3>Specialties:</h3>
                <p><strong>Proficient:</strong> C, GIT, Gitlab</p>
                <p><strong>Intermediate:</strong> C++/C#, HTML, JavaScript, CSS, MySQL, PostgreSQL, PVCS, Canoe/Canalyzer, MKS, IMS, RTC, Trace32, Multi, Jenkins, Linux</p>
                <p><strong>Basic:</strong> Java, PHP, Oracle, Doors, ESI, IMES, CCP/XCP</p>
              </Col>
              <Col md={4}>
                <Image src={robyHeadshot} roundedCircle fluid className="about-me-image" />
              </Col>
            </Row>
          </Container>
        </section>

        <section id="experience" className="py-3 bg-section-2">
          <Container>
            <h2>Work Experience</h2>
            <div className="timeline">
              <div className="timeline-item">
                <div className="timeline-content">
                  <h4>Senior Embedded Software Engineer / Tech Lead Replacement @ Capgemini Services Romania SRL (Capgemini Engineering)</h4>
                  <p className="text-muted">Apr 2022 – Nov 2025</p>
                  <ul>
                    <li>Optimized embedded modules → 20% memory reduction, improved responsiveness, smoother OEM integration.</li>
                    <li>Boosted collaboration → Cut issue resolution time by 30%.</li>
                    <li>Enhanced quality → Refined CAPL tests, reducing post-release bugs by 30%; Google Test improved dependability by 25%.</li>
                    <li>Delivered 300+ Git commits with 100% coding standards compliance → 25% less debugging time.</li>
                    <li>Technical leadership → Acted as Tech Lead, resolving critical roadblocks, mentoring new members, and maintaining project continuity with direct client engagement.</li>
                  </ul>
                </div>
              </div>
              <div className="timeline-item">
                <div className="timeline-content">
                  <h4>Senior Embedded Software Engineer – Space Platforms @ ENEA Software Development Services SRL</h4>
                  <p className="text-muted">Apr 2021 – Apr 2022</p>
                  <ul>
                    <li>Improved real-time performance → Reduced latency via buffer management & interrupt-driven design.</li>
                    <li>Optimized constrained environments → Worked with Xilinx SDK / Zynq-7000 SoC (ARM Cortex-A9).</li>
                    <li>Developed space-grade C/C++ modules → Reliability & fault tolerance focus.</li>
                    <li>Engineered SpaceWire driver interface & state machine for RendezVous Sensor → Enabled real-time telecommand processing.</li>
                    <li>Championed knowledge base of 30+ modules → 20% fewer integration errors, streamlined communication across 3 teams.</li>
                  </ul>
                </div>
              </div>
              <div className="timeline-item">
                <div className="timeline-content">
                  <h4>Senior Embedded Software Engineer – Automotive Platforms @ Visteon Electronics EOOD Sofia, BG – contractor from RINF.TECH</h4>
                  <p className="text-muted">Jun 2014 – May 2020</p>
                  <ul>
                    <li>Led instrument cluster development for Daimler (C/C++) → Improved reliability & user experience.</li>
                    <li>Validated display components with CANoe → Cut test cycle time by 20%.Delivered robust OEM features (Speedometer, Tachometer, Odometer, etc.).</li>
                    <li>Implemented IPC & Franca IDL files → Enabled seamless communication between Application Layer & HMI.Ensured AUTOSAR RTE compliance across projects.</li>
                  </ul>
                </div>
              </div>
              <div className="timeline-item">
                <div className="timeline-content">
                  <h4>Embedded Software Engineer @ Continental Automotive Romania SRL</h4>
                  <p className="text-muted">Aug 2010 – May 2014</p>
                  <ul>
                    <li>Implemented customer-specific C/C++ functionalities across Ford, Renault, VW, Porsche, Audi.</li>
                    <li>Improved diagnostic reliability (DTC, freeze frames, failure reactions) across 5+ OEM platforms.</li>
                    <li>Validated CAN channels & diagnostic instances → Enhanced error management.</li>
                    <li>Reduced field failures via unit & integration testing, documented QA reports.</li>
                    <li>Applied ISO26262 standards in Powertrain systems</li>
                  </ul>
                </div>
              </div>
            </div>
          </Container>
        </section>

        <section id="education" className="py-3 bg-section-7">
          <Container>
            <h2>Education and Certification</h2>
            <div className="timeline">
              <div className="timeline-item">
                <div className="timeline-content">
                  <h3>Faculty of Electronics, Telecommunications and Information Technology, Iasi, Romania</h3>
                  <p>Master’s Degree, Telecommunication Networks · (2009 - 2011)</p>
                </div>
              </div>
              <div className="timeline-item">
                <div className="timeline-content">
                  <h3>Faculty of Economy and Business Administration, "Al.I.Cuza" University, Iasi, Romania</h3>
                  <p>Bachelor’s Degree, Economics and Management · (2007 - 2010)</p>
                </div>
              </div>
              <div className="timeline-item">
                <div className="timeline-content">
                  <h3>Faculty of Automatic Control and Computer Engineering, "Gh.Asachi" University, Iasi, Romania</h3>
                  <p>Bachelor’s Degree, Information Technology · (2005 - 2009)</p>
                </div>
              </div>
              <div className="timeline-item">
                <div className="timeline-content">
                  <h3>"Mihail Kogalniceanu" Highschool, Vaslui, Romania</h3>
                  <p>High School, Mathematics and Computer Science · (2001 - 2005)</p>
                </div>
              </div>
              <div className="timeline-item">
                <div className="timeline-content">
                  <h3>"Stefan cel Mare" School no 5, Vaslui, Romania</h3>
                  <p>Primary School · (1993 - 2001)</p>
                </div>
              </div>
            </div>
          </Container>
        </section>

        <section id="projects" className="py-3 bg-section-3">
          <Container>
            <h2>Projects</h2>
            <p>Here you can showcase your projects.</p>
          </Container>
        </section>

        <section id="skills" className="py-3 bg-section-4">
          <Container>
            <h2>Skills</h2>
            <ul className="list-unstyled">
              <li><strong>Languages & Tools:</strong> ANSI C, C++, CANoe, Trace32, Google Test, Git, Jira, Confluence, CAPL scripting</li>
              <li><strong>Development Models:</strong> V-Cycle, Agile, Scrum</li>
              <li><strong>Protocols & Standards:</strong> CAN, CCP, XCP, AUTOSAR, ISO 26262</li>
              <li><strong>Hardware Expertise:</strong> Xilinx SDK, Zynq-7000 SoC, ARM Cortex-A9</li>
              <li><strong>Expanding Knowledge:</strong> Python, C#, Rust</li>
            </ul>
          </Container>
        </section>

        <section id="languages" className="py-3 bg-section-5">
          <Container>
            <h2>Languages</h2>
            <Row>
              <Col md={6}>
                <Table striped bordered hover>
                  <thead>
                    <tr>
                      <th>Language</th>
                      <th>Proficiency</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>Romanian</td>
                      <td>Native</td>
                    </tr>
                    <tr>
                      <td>English</td>
                      <td>C2</td>
                    </tr>
                    <tr>
                      <td>German</td>
                      <td>B1</td>
                    </tr>
                  </tbody>
                </Table>
              </Col>
            </Row>
          </Container>
        </section>

        <section id="contact" className="py-3 bg-section-6">
          <Container>
            <h2>Contact</h2>
            <p><strong>Mobile: +40 760 827 250</strong></p>
            <p>Email: <a href="mailto:filipescurobert@gmail.com">filipescurobert@gmail.com</a></p>
          </Container>
        </section>
      </main>

      <footer className="bg-dark text-white text-center py-3">
        <Container>
          <p>&copy; 2025 Robert</p>
        </Container>
      </footer>
    </>
  );
}

export default App;