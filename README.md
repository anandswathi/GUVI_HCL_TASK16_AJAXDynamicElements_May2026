# GUVI_HCL_TASK16_AJAXDynamicElements_May2026
GUVI HCLTASK 16 - AJAX Dynamic Elements

The current repository contains python codes to the questions mentioned in HCL GUVI Python Task 16 - https://docs.google.com/document/d/1FQNA2p-0B62jvtSBBYJY4VSp333Gd2j1RGpwMaftJVc/edit?tab=t.0

============================================================================================================================================================

Project Structure POM for WORLD POPULATION
world_population/
├── conftest.py                         ← Driver fixture + screenshot hook
├── pytest.ini                          ← Pytest config and markers
├── requirements.txt
│
├── drivers/
│   └── driver_factory.py               ← Chrome/Edge/Firefox factory
│
├── pages/
│   ├── base_page.py                    ← Explicit Wait + EC wrappers
│   └── population_clock_page.py        ← POM for the live counter page
│
├── tests/
│   └── test_population_clock.py        ← 3 test cases + live polling loop
│
└── utils/
    └── logger.py                       ← Console + file logging
