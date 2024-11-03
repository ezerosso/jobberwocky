from typing import Dict

class SearchMatcher:
    @staticmethod
    def matches_pattern(job_data: Dict, search_pattern: str) -> bool:
        if not search_pattern:
            return True

        patterns = [p.strip().lower() for p in search_pattern.split(',')]
        
        searchable_content = [
            job_data.get('title', '').lower(),
            job_data.get('description', '').lower(),
            job_data.get('company', '').lower(),
            *[skill.lower() for skill in job_data.get('skills', [])]
        ]
        
        combined_content = ' '.join(searchable_content)
        
        return all(pattern in combined_content for pattern in patterns)