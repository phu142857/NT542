#!/usr/bin/env python3
"""
Extract OpenSCAP rule results from XML report and generate LaTeX table
"""

import xml.etree.ElementTree as ET
import re
import sys

def extract_rules_from_xml(xml_file):
    """Extract rule titles and results from OpenSCAP XML report"""
    
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
        return []
    
    # Define XML namespaces
    ns = {
        'xccdf': 'http://checklists.nist.gov/xccdf/1.2'
    }
    
    results = []
    
    for rule_result in root.findall(".//xccdf:rule-result", ns):
        try:
            rule_id = rule_result.get("idref")
            
            result_elem = rule_result.find("xccdf:result", ns)
            result_text = result_elem.text if result_elem is not None else None
            
            severity = rule_result.get("severity") or "medium"
            
            # Normalize result
            result = 'unknown'
            if result_text:
                result_lower = result_text.lower()
                if 'pass' in result_lower:
                    result = 'pass'
                elif 'fail' in result_lower:
                    result = 'fail'
                elif 'error' in result_lower or 'notchecked' in result_lower:
                    result = 'other'
            
            # Try to find the rule title by looking up the rule definition
            title = f"Rule {rule_id}"  # Default fallback
            
            # Try to find the rule definition elsewhere in the document first
            rule_def = root.find(f".//xccdf:rule[@id='{rule_id}']", ns)
            if rule_def is not None:
                title_elem = rule_def.find(".//title", ns)
                if title_elem is not None and title_elem.text:
                    title = title_elem.text.strip()
            else:
                # Look for title in the current rule-result as fallback
                title_elem = rule_result.find(".//title", ns)
                if title_elem is not None and title_elem.text:
                    title = title_elem.text.strip()
            
            # Skip non-rule titles
            if 'Compliance and Scoring' in title or 'Guide to the Secure Configuration' in title:
                continue
            
            if result != 'unknown' and title:
                results.append({
                    'title': title,
                    'severity': severity,
                    'result': result,
                    'id': rule_id
                })
                
        except Exception as e:
            print(f"Error processing rule: {e}")
            continue
    
    return results

def generate_latex_table(rules, output_file):
    """Generate LaTeX table from extracted rules using longtable for multi-page support"""
    
    # Filter rules to only include pass/fail results
    filtered_rules = [r for r in rules if r['result'] in ['pass', 'fail']]
    
    # Sort by result (pass first) and then by title
    filtered_rules.sort(key=lambda x: (x['result'] != 'pass', x['title']))
    
    latex_content = []
    
    # Add longtable package requirement comment
    latex_content.append("% Use longtable for multi-page table support")
    latex_content.append("% Add \\usepackage{longtable} to preamble if not already present")
    latex_content.append("")
    
    # Begin longtable with proper headers
    latex_content.append("\\begin{longtable}{|p{10cm}|p{2cm}|p{2cm}|}")
    latex_content.append("\\caption{Toàn bộ kết quả đánh giá OpenSCAP (pass/fail)} \\label{tab:openscap-all-results} \\\\")
    latex_content.append("")
    
    # First page header
    latex_content.append("\\hline")
    latex_content.append("\\textbf{Title} & \\textbf{Severity} & \\textbf{Result} \\\\")
    latex_content.append("\\hline")
    latex_content.append("\\endfirsthead")
    latex_content.append("")
    
    # Subsequent pages header
    latex_content.append("\\multicolumn{3}{c}%")
    latex_content.append("{{\\bfseries \\tablename\\ \\thetable{} -- continued from previous page}} \\\\")
    latex_content.append("\\hline")
    latex_content.append("\\textbf{Title} & \\textbf{Severity} & \\textbf{Result} \\\\")
    latex_content.append("\\hline")
    latex_content.append("\\endhead")
    latex_content.append("")
    
    # Footer for pages except last
    latex_content.append("\\hline")
    latex_content.append("\\multicolumn{3}{r}{{Continued on next page}} \\\\")
    latex_content.append("\\endfoot")
    latex_content.append("")
    
    # Footer for last page
    latex_content.append("\\hline")
    latex_content.append("\\endlastfoot")
    latex_content.append("")
    
    # Add all results in one continuous table (no separation)
    for rule in filtered_rules:
        # Extract rule name by removing prefix
        title = rule['title']
        if title.startswith('Rule xccdf_org.ssgproject.content_rule_'):
            title = title.replace('Rule xccdf_org.ssgproject.content_rule_', '')
        elif title.startswith('xccdf_org.ssgproject.content_rule_'):
            title = title.replace('xccdf_org.ssgproject.content_rule_', '')
        
        # Escape special LaTeX characters in title
        title = title.replace('_', '\\_').replace('&', '\\&').replace('%', '\\%').replace('$', '\\$').replace('#', '\\#')
            
        severity = rule['severity']
        result = rule['result']
        
        latex_content.append(f"{title} & {severity} & {result} \\\\")
        latex_content.append("\\hline")
    
    # End longtable
    latex_content.append("\\end{longtable}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(latex_content))
    
    print(f"Generated LaTeX longtable with {len(filtered_rules)} rules")
    print(f"File saved to: {output_file}")
    
    # Print statistics
    pass_count = len([r for r in filtered_rules if r['result'] == 'pass'])
    fail_count = len([r for r in filtered_rules if r['result'] == 'fail'])
    print(f"\nStatistics:")
    print(f"Pass: {pass_count}")
    print(f"Fail: {fail_count}")
    print(f"Total: {len(filtered_rules)}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 extract_openscap_xml.py <xml_file>")
        sys.exit(1)
    
    xml_file = sys.argv[1]
    output_file = 'openscap_results_table.tex'
    
    print(f"Extracting rules from: {xml_file}")
    rules = extract_rules_from_xml(xml_file)
    
    print(f"Found {len(rules)} total rules")
    
    if not rules:
        print("No rules found. Let me examine the XML structure...")
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            print(f"Root element: {root.tag}")
            print("First few child elements:")
            for i, child in enumerate(root):
                if i < 10:
                    print(f"  {i}: {child.tag}")
                else:
                    break
        except Exception as e:
            print(f"Error examining XML: {e}")
        return
    
    # Generate LaTeX table
    generate_latex_table(rules, output_file)
    
    # Print first 10 rules for verification
    print("\nFirst 10 rules:")
    for i, rule in enumerate(rules[:10]):
        title_preview = rule['title'][:60] + '...' if len(rule['title']) > 60 else rule['title']
        print(f"{i+1}. {title_preview} - {rule['severity']} - {rule['result']}")

if __name__ == "__main__":
    main()
