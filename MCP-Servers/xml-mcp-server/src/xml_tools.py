from lxml import etree
from xmlschema import XMLSchema, XMLSchemaException
import os       
from typing import Any, Dict, List, Optional
from difflib import unified_diff

def validate_xml_against_xsd(xml_file: str, xsd_file: str) -> Dict[str, Any]:
    """Validate XML document against XSD schema"""
    try:
        if not os.path.exists(xml_file):
            return {"error": f"XML file not found: {xml_file}"}
        if not os.path.exists(xsd_file):
            return {"error": f"XSD file not found: {xsd_file}"}
        
        schema = XMLSchema(xsd_file)
        is_valid = schema.is_valid(xml_file)
        
        if not is_valid:
            errors = [str(e) for e in schema.iter_errors(xml_file)]
            return {
                "valid": False,
                "errors": errors
            }
        
        return {"valid": True, "message": "XML document is valid"}
    
    except Exception as e:
        return {"error": str(e)}

def parse_xml_tree(xml_file: str, max_depth: Optional[int] = None) -> Dict[str, Any]:
    """Parse XML and return tree structure"""
    try:
        if not os.path.exists(xml_file):
            return {"error": f"XML file not found: {xml_file}"}
        
        tree = etree.parse(xml_file)
        root = tree.getroot()
        
        def build_tree(element, depth=0):
            if max_depth and depth >= max_depth:
                return None
            
            node = {
                "tag": element.tag,
                "attributes": dict(element.attrib),
                "text": (element.text or "").strip(),
                "tail": (element.tail or "").strip(),
                "children": []
            }
            
            for child in element:
                child_node = build_tree(child, depth + 1)
                if child_node:
                    node["children"].append(child_node)
            
            return node
        
        return {
            "tree": build_tree(root),
            "encoding": tree.docinfo.encoding or "UTF-8"
        }
    
    except Exception as e:
        return {"error": str(e)}

def query_xml_xpath(xml_file: str, xpath: str) -> Dict[str, Any]:
    """Query XML using XPath expression"""
    try:
        if not os.path.exists(xml_file):
            return {"error": f"XML file not found: {xml_file}"}
        
        tree = etree.parse(xml_file)
        root = tree.getroot()
        
        results = root.xpath(xpath)
        
        formatted_results = []
        for result in results:
            if isinstance(result, etree._Element):
                formatted_results.append({
                    "tag": result.tag,
                    "text": (result.text or "").strip(),
                    "attributes": dict(result.attrib)
                })
            else:
                formatted_results.append(str(result))
        
        return {
            "query": xpath,
            "count": len(results),
            "results": formatted_results
        }
    
    except Exception as e:
        return {"error": str(e)}

def transform_xml_xslt(xml_file: str, xslt_file: str) -> Dict[str, Any]:
    """Transform XML using XSLT stylesheet"""
    try:
        if not os.path.exists(xml_file):
            return {"error": f"XML file not found: {xml_file}"}
        if not os.path.exists(xslt_file):
            return {"error": f"XSLT file not found: {xslt_file}"}
        
        xml_doc = etree.parse(xml_file)
        xslt_doc = etree.parse(xslt_file)
        transform = etree.XSLT(xslt_doc)
        result = transform(xml_doc)
        
        return {
            "result": str(result),
            "success": True
        }
    
    except Exception as e:
        return {"error": str(e)}

def format_xml(xml_file: str, indent: int = 2) -> Dict[str, Any]:
    """Format and prettify XML document"""
    try:
        if not os.path.exists(xml_file):
            return {"error": f"XML file not found: {xml_file}"}
        
        tree = etree.parse(xml_file)
        root = tree.getroot()
        
        formatted = etree.tostring(
            root,
            pretty_print=True,
            encoding="unicode",
            xml_declaration=True
        )
        
        return {
            "formatted_xml": formatted,
            "success": True
        }
    
    except Exception as e:
        return {"error": str(e)}

def generate_xml_schema(xml_file: str, output_file: str) -> Dict[str, Any]:
    """Generate XSD schema from XML document"""
    try:
        if not os.path.exists(xml_file):
            return {"error": f"XML file not found: {xml_file}"}
        
        schema = XMLSchema.meta_schema
        tree = etree.parse(xml_file)
        root = tree.getroot()
        
        # Create basic schema structure
        schema_root = etree.Element(
            "{http://www.w3.org/2001/XMLSchema}schema",
            xmlns="http://www.w3.org/2001/XMLSchema"
        )
        
        def extract_element_info(element, depth=0):
            if depth > 5:  # Limit recursion
                return
            
            elem_def = etree.SubElement(
                schema_root,
                "{http://www.w3.org/2001/XMLSchema}element",
                name=element.tag.split("}")[-1],
                type="xs:string"
            )
            
            for child in element:
                extract_element_info(child, depth + 1)
        
        extract_element_info(root)
        
        schema_str = etree.tostring(
            schema_root,
            pretty_print=True,
            encoding="unicode",
            xml_declaration=True
        )
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(schema_str)
        
        return {
            "output_file": output_file,
            "message": "Schema generated successfully"
        }
    
    except Exception as e:
        return {"error": str(e)}

def compare_xml_documents(xml_file1: str, xml_file2: str) -> Dict[str, Any]:
    """Compare two XML documents"""
    try:
        if not os.path.exists(xml_file1):
            return {"error": f"XML file not found: {xml_file1}"}
        if not os.path.exists(xml_file2):
            return {"error": f"XML file not found: {xml_file2}"}
        
        tree1 = etree.parse(xml_file1)
        tree2 = etree.parse(xml_file2)
        
        str1 = etree.tostring(tree1, pretty_print=True, encoding="unicode").splitlines()
        str2 = etree.tostring(tree2, pretty_print=True, encoding="unicode").splitlines()
        
        diff = list(unified_diff(str1, str2, lineterm=''))
        
        are_equal = tree1.getroot().tag == tree2.getroot().tag and len(diff) == 0
        
        return {
            "equal": are_equal,
            "differences": diff if diff else [],
            "diff_count": len(diff)
        }
    
    except Exception as e:
        return {"error": str(e)}

def extract_xml_namespaces(xml_file: str) -> Dict[str, Any]:
    """Extract all namespaces from XML document"""
    try:
        if not os.path.exists(xml_file):
            return {"error": f"XML file not found: {xml_file}"}
        
        tree = etree.parse(xml_file)
        root = tree.getroot()
        
        namespaces = {}
        
        def collect_namespaces(element):
            for prefix, uri in element.nsmap.items():
                key = prefix if prefix else "default"
                if uri not in namespaces.values():
                    namespaces[key] = uri
            
            for child in element:
                collect_namespaces(child)
        
        collect_namespaces(root)
        
        return {
            "namespaces": namespaces,
            "count": len(namespaces)
        }
    
    except Exception as e:
        return {"error": str(e)}
