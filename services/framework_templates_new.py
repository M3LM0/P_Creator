"""
Templates de frameworks pour P_Creator
Reproduit l'expérience PyCharm/PhpStorm avec des structures complètes
"""

import os
from typing import Dict, List, Any

# Import des templates spécialisés
from .templates.python_templates import get_python_templates
from .templates.js_templates import get_js_templates
from .templates.php_templates import get_php_templates

class FrameworkTemplates:
    """Gestionnaire des templates de frameworks"""
    
    def __init__(self):
        """Initialise les templates depuis les fichiers spécialisés"""
        self._templates = {
            "Python": get_python_templates(),
            "JavaScript": get_js_templates(),
            "PHP": get_php_templates()
        }
    
    @classmethod
    def get_languages(cls) -> List[str]:
        """Retourne la liste des langages supportés"""
        return ["Python", "JavaScript", "PHP"]
    
    @classmethod
    def get_frameworks(cls, language: str) -> List[Dict[str, Any]]:
        """Retourne la liste des frameworks pour un langage"""
        instance = cls()
        if language not in instance._templates:
            return []
        
        frameworks = []
        for key, template in instance._templates[language].items():
            frameworks.append({
                "key": key,
                "name": template["name"],
                "description": template["description"]
            })
        return frameworks
    
    @classmethod
    def get_template(cls, language: str, framework: str) -> Dict[str, Any]:
        """Retourne le template complet pour un framework"""
        instance = cls()
        if language not in instance._templates:
            raise ValueError(f"Langage {language} non supporté")
        
        if framework not in instance._templates[language]:
            raise ValueError(f"Framework {framework} non supporté pour {language}")
        
        return instance._templates[language][framework]
    
    @classmethod
    def get_dependencies(cls, language: str, framework: str) -> List[str]:
        """Retourne les dépendances pour un framework"""
        template = cls.get_template(language, framework)
        return template.get("dependencies", [])
    
    @classmethod
    def get_run_command(cls, language: str, framework: str) -> str:
        """Retourne la commande de lancement pour un framework"""
        template = cls.get_template(language, framework)
        return template.get("run_command", "")
    
    @classmethod
    def get_dev_port(cls, language: str, framework: str) -> int:
        """Retourne le port de développement pour un framework"""
        template = cls.get_template(language, framework)
        return template.get("dev_port", 8000)
    
    @classmethod
    def get_available_frameworks(cls) -> Dict[str, List[str]]:
        """Retourne tous les frameworks disponibles par langage"""
        instance = cls()
        result = {}
        for language, templates in instance._templates.items():
            result[language] = list(templates.keys())
        return result
    
    @classmethod
    def get_framework_info(cls, language: str, framework: str) -> Dict[str, Any]:
        """Retourne les informations détaillées d'un framework"""
        template = cls.get_template(language, framework)
        return {
            "name": template["name"],
            "description": template["description"],
            "dependencies": template.get("dependencies", []),
            "run_command": template.get("run_command", ""),
            "dev_port": template.get("dev_port", 8000),
            "structure": template.get("structure", {})
        }
    
    @classmethod
    def validate_framework(cls, language: str, framework: str) -> bool:
        """Valide qu'un framework existe pour un langage donné"""
        try:
            cls.get_template(language, framework)
            return True
        except ValueError:
            return False
    
    @classmethod
    def get_framework_count(cls) -> int:
        """Retourne le nombre total de frameworks disponibles"""
        instance = cls()
        total = 0
        for templates in instance._templates.values():
            total += len(templates)
        return total
    
    @classmethod
    def get_language_framework_count(cls, language: str) -> int:
        """Retourne le nombre de frameworks pour un langage"""
        instance = cls()
        if language not in instance._templates:
            return 0
        return len(instance._templates[language])
    
    @classmethod
    def search_frameworks(cls, query: str) -> List[Dict[str, str]]:
        """Recherche des frameworks par nom ou description"""
        instance = cls()
        results = []
        query_lower = query.lower()
        
        for language, templates in instance._templates.items():
            for key, template in templates.items():
                if (query_lower in template["name"].lower() or 
                    query_lower in template["description"].lower()):
                    results.append({
                        "language": language,
                        "key": key,
                        "name": template["name"],
                        "description": template["description"]
                    })
        
        return results
    
    @classmethod
    def get_frameworks_by_category(cls) -> Dict[str, List[Dict[str, str]]]:
        """Retourne les frameworks organisés par catégorie"""
        instance = cls()
        categories = {
            "Web Backend": [],
            "Web Frontend": [],
            "Mobile": [],
            "API": []
        }
        
        for language, templates in instance._templates.items():
            for key, template in templates.items():
                framework_info = {
                    "language": language,
                    "key": key,
                    "name": template["name"],
                    "description": template["description"]
                }
                
                # Classification basée sur le nom et la description
                name_lower = template["name"].lower()
                desc_lower = template["description"].lower()
                
                if "mobile" in desc_lower or "native" in desc_lower:
                    categories["Mobile"].append(framework_info)
                elif "api" in desc_lower or "express" in name_lower or "fastapi" in name_lower:
                    categories["API"].append(framework_info)
                elif any(frontend in name_lower for frontend in ["react", "vue", "angular"]):
                    categories["Web Frontend"].append(framework_info)
                else:
                    categories["Web Backend"].append(framework_info)
        
        return categories


