"""
Topic discovery and filtering.

Responsibilities:
- Query ROS2 graph for topics
- Apply include/exclude patterns
- Determine message types and QoS
- Handle dynamic topic changes
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
import re

dataclass
class TopicInfo:
    """Information about a discovered topic."""
    name: str
    message_type: str
    qos: Dict
    publisher_count: int

class TopicDiscovery:
    """Discovers and filters ROS2 topics."""
    
    def __init__(self, node, config: Dict):
        """
        Initialize topic discovery.
        
        Args:
            node: ROS2 node instance
            config: Discovery configuration
        """
        self.node = node
        self.config = config
        self.include_patterns = [re.compile(p) for p in config.get('include_patterns', [])]
        self.exclude_patterns = [re.compile(p) for p in config.get('exclude_patterns', [])]
        self.priority_topics = config.get('priority_topics', [])
        
    def discover_topics(self) -> List[TopicInfo]:
        """
        Discover all available topics.
        
        Returns:
            List of discovered topics with metadata
        """
        # Query ROS2 graph
        # Get topic names, types, QoS
        # Apply filters
        # Sort by priority
        pass
        
    def get_topic_type(self, topic: str) -> str:
        """
        Get message type for a topic.
        
        Args:
            topic: Topic name
            
        Returns:
            Fully qualified message type
        """
        # Query topic type from ROS2
        pass
        
    def get_topic_qos(self, topic: str) -> Dict:
        """
        Determine QoS settings for a topic.
        
        Args:
            topic: Topic name
            
        Returns:
            QoS profile dictionary
        """
        # Check for override in config
        # Otherwise use defaults
        # Query existing publishers for compatibility
        pass
        
    def filter_topics(self, topics: List[str]) -> List[str]:
        """
        Apply include/exclude filters to topic list.
        
        Args:
            topics: List of topic names
            
        Returns:
            Filtered list of topic names
        """
        filtered = []
        for topic in topics:
            # Check exclude patterns
            if any(p.match(topic) for p in self.exclude_patterns):
                continue
            # Check include patterns (if any specified)
            if self.include_patterns:
                if any(p.match(topic) for p in self.include_patterns):
                    filtered.append(topic)
            else:
                filtered.append(topic)
        return filtered
