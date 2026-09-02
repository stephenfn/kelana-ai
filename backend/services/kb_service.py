"""
Knowledge Base Service
Handles RAG (Retrieval-Augmented Generation) operations with Amazon Bedrock
"""

import json
import os
from typing import Optional

try:
    import boto3
except ImportError:
    boto3 = None


class KnowledgeBaseService:
    """Service for interacting with Amazon Bedrock Knowledge Base"""
    
    def __init__(self):
        """Initialize Bedrock client and Knowledge Base configuration"""
        self.knowledge_base_id = os.getenv("BEDROCK_KB_ID", "your-kb-id")
        self.region = os.getenv("AWS_REGION", "us-east-1")
        
        if boto3:
            self.client = boto3.client("bedrock-agent-runtime", region_name=self.region)
        else:
            self.client = None
    
    def ask_knowledge_base(self, question: str, retrieve_only: bool = False) -> dict:
        """
        Query the Knowledge Base with a question.
        
        Args:
            question: The question to ask
            retrieve_only: If True, only retrieve documents without generating
            
        Returns:
            Dictionary containing answer and optionally source metadata
        """
        if not self.client:
            # Demo mode - return mock response
            return self._get_mock_response(question)
        
        try:
            # Use retrieve_and_generate for full RAG pipeline
            if retrieve_only:
                response = self.client.retrieve(
                    knowledgeBaseId=self.knowledge_base_id,
                    retrievalQuery={"text": question},
                    retrievalConfiguration={
                        "managedSearchConfiguration": {
                            "numberOfResults": 5,
                        },
                    },
                )
                return {
                    "success": True,
                    "sources": response.get("retrievalResults", []),
                    "answer": None
                }
            else:
                # Full retrieve and generate
                response = self.client.retrieve_and_generate(
                    input={"text": question},
                    retrieveAndGenerateConfiguration={
                        "type": "KNOWLEDGE_BASE",
                        "knowledgeBaseConfiguration": {
                            "knowledgeBaseId": self.knowledge_base_id,
                            "modelArn": "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet",
                            "retrievalConfiguration": {
                                "vectorSearchConfiguration": {
                                    "numberOfResults": 5,
                                }
                            },
                        }
                    }
                )
                
                # Extract answer and citations
                answer_text = response["output"]["text"]
                citations = []
                
                if "citations" in response:
                    for citation in response["citations"]:
                        if "retrievedReferences" in citation:
                            for ref in citation["retrievedReferences"]:
                                citations.append({
                                    "document": ref.get("document", {}).get("title", "Unknown"),
                                    "source": ref.get("document", {}).get("source", "")
                                })
                
                return {
                    "success": True,
                    "answer": answer_text,
                    "sources": citations
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "answer": None
            }
    
    def _get_mock_response(self, question: str) -> dict:
        """
        Returns mock response when AWS credentials are not available.
        Useful for testing without AWS setup.
        """
        # Mock responses based on question keywords
        mock_responses = {
            "visa": {
                "answer": "Indonesian passport holders need a tourist visa to visit Japan. As of 2025, you can apply for an e-visa online or at the Japanese embassy. Processing typically takes 5-7 business days. Required documents include a valid passport, completed visa application form, and proof of travel arrangements.",
                "sources": [{"document": "visa-japan.pdf", "source": "Travel Documents Required"}]
            },
            "baggage": {
                "answer": "Standard baggage allowance for most international carriers is typically 23kg (50lbs) for checked baggage and 7kg (15lbs) for carry-on. However, baggage policies vary by airline. Please check your specific flight confirmation for exact limits. Excess baggage fees typically range from $15-50 per kg depending on the carrier.",
                "sources": [{"document": "packing-checklist.pdf", "source": "Travel Tips and Packing"}]
            },
            "insurance": {
                "answer": "Travel insurance typically covers medical emergencies, trip cancellations, lost luggage, and travel delays. Premium costs range from $50-200 depending on trip duration and coverage level. We recommend purchasing insurance within 14 days of your initial trip deposit. Coverage usually excludes pre-existing conditions and high-risk activities.",
                "sources": [{"document": "travel-insurance.pdf", "source": "Insurance Policy Details"}]
            },
            "attraction": {
                "answer": "Tokyo's top attractions include Senso-ji Temple in Asakusa, Meiji Shrine in Shibuya, Tokyo Skytree for panoramic views, and teamLab Borderless for immersive digital art. Shibuya Crossing is the world's busiest pedestrian crossing. Allow 2-3 days to experience the main attractions. Most attractions are accessible by train and reasonably priced.",
                "sources": [{"document": "tokyo-attractions.pdf", "source": "Tokyo Travel Guide"}]
            }
        }
        
        # Find best matching response
        question_lower = question.lower()
        for keyword, response in mock_responses.items():
            if keyword in question_lower:
                return {
                    "success": True,
                    "answer": response["answer"],
                    "sources": response["sources"]
                }
        
        # Default response
        return {
            "success": True,
            "answer": "Based on our travel knowledge base, I don't have specific information to answer this question. Please rephrase your question or contact our support team for assistance.",
            "sources": []
        }


# Singleton instance
_kb_service = None


def get_kb_service() -> KnowledgeBaseService:
    """Get or create singleton instance of KnowledgeBaseService"""
    global _kb_service
    if _kb_service is None:
        _kb_service = KnowledgeBaseService()
    return _kb_service
