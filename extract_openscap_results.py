#!/usr/bin/env python3
"""
Extract OpenSCAP rule results from HTML report and generate LaTeX table
"""

import re
import sys
from html.parser import HTMLParser

class OpenSCAPParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rules = []
        self.current_rule = {}
        self.in_rule_section = False
        self.in_title = False
        self.in_description = False
        self.in_result = False
        self.current_text = ''
        self.severity = 'unknown'
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        # Detect rule sections
        if tag == 'div' and 'class' in attrs_dict:
            if 'rule-result' in attrs_dict['class']:
                self.in_rule_section = True
                self.current_rule = {'title': '', 'severity': 'unknown', 'result': 'unknown'}
        
        # Detect title
        if tag == 'h2' and self.in_rule_section:
            self.in_title = True
            self.current_text = ''
            
        # Detect severity
        if tag == 'span' and 'class' in attrs_dict and self.in_rule_section:
            if 'label-danger' in attrs_dict['class']:
                self.current_rule['result'] = 'fail'
            elif 'label-success' in attrs_dict['class']:
                self.current_rule['result'] = 'pass'
            elif 'label-warning' in attrs_dict['class']:
                self.current_rule['result'] = 'other'
                
    def handle_endtag(self, tag):
        if tag == 'div' and self.in_rule_section:
            if self.current_rule['title']:
                self.rules.append(self.current_rule)
            self.in_rule_section = False
            
        if tag == 'h2' and self.in_title:
            self.current_rule['title'] = self.current_text.strip()
            self.in_title = False
            
    def handle_data(self, data):
        if self.in_title:
            self.current_text += data

def extract_rules_from_html(html_file):
    """Extract rule titles and results from OpenSCAP HTML report"""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Look for rule sections with titles and results
    # OpenSCAP reports have specific structure: rule title in <h2>, then result badges
    rules = []
    
    # Find all rule sections by looking for <h2> tags that contain rule titles
    h2_pattern = r'<h2[^>]*>(.*?)</h2>(.*?)(?=<h2>|$)'
    h2_matches = re.findall(h2_pattern, content, re.DOTALL)
    
    for title, section_content in h2_matches:
        # Skip non-rule sections
        if 'Compliance and Scoring' in title or 'Guide to the Secure Configuration' in title:
            continue
            
        # Clean HTML tags from title
        clean_title = re.sub(r'<[^>]+>', '', title).strip()
        
        if not clean_title or len(clean_title) < 10:  # Skip very short titles
            continue
        
        # Determine result from the section content
        result = 'unknown'
        if 'label-success' in section_content:
            result = 'pass'
        elif 'label-danger' in section_content:
            result = 'fail'
        elif 'label-warning' in section_content:
            result = 'other'
        
        # Extract severity from the section
        severity = 'medium'  # Default
        if 'severity.*high' in section_content.lower() or 'high.*severity' in section_content.lower():
            severity = 'high'
        elif 'severity.*low' in section_content.lower() or 'low.*severity' in section_content.lower():
            severity = 'low'
        
        # Also check for specific severity indicators
        if 'label-danger' in section_content and 'high' in section_content.lower():
            severity = 'high'
        elif 'label-info' in section_content and 'low' in section_content.lower():
            severity = 'low'
        elif 'label-warning' in section_content and 'medium' in section_content.lower():
            severity = 'medium'
        
        rules.append({
            'title': clean_title,
            'severity': severity,
            'result': result
        })
    
    # Alternative method: look for specific rule result patterns
    # This catches rules that might be missed by the h2 approach
    alt_pattern = r'<div[^>]*class="[^"]*rule-result[^"]*"[^>]*>.*?<h2[^>]*>(.*?)</h2>.*?(label-success|label-danger|label-warning)'
    alt_matches = re.findall(alt_pattern, content, re.DOTALL)
    
    for title, result_label in alt_matches:
        clean_title = re.sub(r'<[^>]+>', '', title).strip()
        
        if not clean_title or len(clean_title) < 10:
            continue
            
        # Check if we already have this rule
        if not any(r['title'] == clean_title for r in rules):
            result = 'pass' if 'success' in result_label else 'fail' if 'danger' in result_label else 'other'
            
            rules.append({
                'title': clean_title,
                'severity': 'medium',  # Default for alt method
                'result': result
            })
    
    return rules

def generate_latex_table(rules, output_file):
    """Generate LaTeX table from extracted rules"""
    
    # Filter rules to only include pass/fail results
    filtered_rules = [r for r in rules if r['result'] in ['pass', 'fail']]
    
    # Sort by result (pass first) and then by title
    filtered_rules.sort(key=lambda x: (x['result'] != 'pass', x['title']))
    
    latex_content = []
    latex_content.append("\\begin{table}[H]")
    latex_content.append("\\centering")
    latex_content.append("\\footnotesize")
    latex_content.append("\\renewcommand{\\arraystretch}{1.2}")
    latex_content.append("\\begin{tabular}{|p{8cm}|p{2cm}|p{2cm}|}")
    latex_content.append("\\hline")
    latex_content.append("\\textbf{Title} & \\textbf{Severity} & \\textbf{Result} \\\\")
    latex_content.append("\\hline")
    
    for rule in filtered_rules:
        # Escape special LaTeX characters in title
        title = rule['title'].replace('_', '\\_').replace('&', '\\&').replace('%', '\\%').replace('$', '\\$')
        # Truncate very long titles
        if len(title) > 70:
            title = title[:67] + '...'
            
        severity = rule['severity']
        result = rule['result']
        
        latex_content.append(f"{title} & {severity} & {result} \\\\")
        latex_content.append("\\hline")
    
    latex_content.append("\\end{tabular}")
    latex_content.append("\\caption{Toàn bộ kết quả đánh giá OpenSCAP (pass/fail)}")
    latex_content.append("\\label{tab:openscap-all-results}")
    latex_content.append("\\end{table}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(latex_content))
    
    print(f"Generated LaTeX table with {len(filtered_rules)} rules")
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
        print("Usage: python3 extract_openscap_results.py <html_file>")
        sys.exit(1)
    
    html_file = sys.argv[1]
    output_file = 'openscap_results_table.tex'
    
    print(f"Extracting rules from: {html_file}")
    rules = extract_rules_from_html(html_file)
    
    print(f"Found {len(rules)} total rules")
    
    # Generate LaTeX table
    generate_latex_table(rules, output_file)
    
    # Also print first 10 rules for verification
    print("\nFirst 10 rules:")
    for i, rule in enumerate(rules[:10]):
        print(f"{i+1}. {rule['title'][:60]}... - {rule['severity']} - {rule['result']}")

if __name__ == "__main__":
    main()
