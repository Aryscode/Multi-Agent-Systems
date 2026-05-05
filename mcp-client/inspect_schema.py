#!/usr/bin/env python3
"""Inspect schema structure."""

from xml.etree import ElementTree as ET

tree = ET.parse(r'd:\Projects\Multi-Agent-Systems\mcp-client\AUTOSAR_4-3-1.xsd')
root = tree.getroot()

ns = {'xs': 'http://www.w3.org/2001/XMLSchema'}

# Find AR:AUTOSAR type definition
types = root.findall('.//xs:complexType[@name="AUTOSAR"]', ns)
if types:
    print('Found AUTOSAR complexType')
    type_elem = types[0]
    # Find sequence
    seqs = type_elem.findall('.//xs:sequence', ns)
    if seqs:
        seq = seqs[0]
        elements = seq.findall('xs:element', ns)
        print(f'Found {len(elements)} child elements')
        for elem in elements[:10]:
            print(f'  - {elem.get("name")}: minOccurs={elem.get("minOccurs", "1")}, type={elem.get("type", "N/A")}')
    else:
        print('No sequence found')
else:
    print('AUTOSAR complexType not found')
    # Try group references
    groups = root.findall('.//xs:group[@name="AUTOSAR"]', ns)
    if groups:
        print(f'Found AUTOSAR group')
        group = groups[0]
        seqs = group.findall('.//xs:sequence', ns)
        if seqs:
            seq = seqs[0]
            elements = seq.findall('xs:element', ns)
            print(f'Found {len(elements)} child elements in group')
            for elem in elements[:10]:
                print(f'  - {elem.get("name")}: minOccurs={elem.get("minOccurs", "1")}, type={elem.get("type", "N/A")}')
