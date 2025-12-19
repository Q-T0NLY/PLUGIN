"""
Advanced Multi-Factor Scoring Engine.
Computes composite scores for discoveries and resources across multiple dimensions:
health, relevance, performance, security, reliability.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
import math


class ScoreDimension(Enum):
    HEALTH = "health"
    RELEVANCE = "relevance"
    PERFORMANCE = "performance"
    SECURITY = "security"
    RELIABILITY = "reliability"
    AVAILABILITY = "availability"


@dataclass
class DimensionScore:
    """Score for a single dimension."""
    dimension: ScoreDimension
    value: float  # 0-100
    weight: float  # importance weight
    factors: Dict[str, float] = field(default_factory=dict)  # contributing factors
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CompositeScore:
    """Composite score with breakdown by dimension."""
    entity_id: str
    entity_name: str
    overall_score: float  # 0-100, weighted average
    dimension_scores: Dict[str, DimensionScore] = field(default_factory=dict)
    trend: str = "stable"  # stable, improving, declining
    rating: str = "good"  # excellent, good, fair, poor
    recommendations: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class AdvancedScoringEngine:
    """
    Advanced scoring engine for multi-factor evaluation of discoveries and resources.
    """
    
    def __init__(self):
        # Default weights for dimensions
        self.dimension_weights = {
            ScoreDimension.HEALTH: 0.25,
            ScoreDimension.RELEVANCE: 0.20,
            ScoreDimension.PERFORMANCE: 0.20,
            ScoreDimension.SECURITY: 0.20,
            ScoreDimension.RELIABILITY: 0.10,
            ScoreDimension.AVAILABILITY: 0.05
        }
        
        self.score_history: Dict[str, List[CompositeScore]] = {}
        self.thresholds = {
            'excellent': 90,
            'good': 75,
            'fair': 60,
            'poor': 0
        }
    
    def compute_health_score(self, metrics: Dict[str, Any]) -> DimensionScore:
        """Compute health score from metrics."""
        factors = {}
        
        # CPU health (0-100 where 100 = not overloaded)
        cpu = metrics.get('cpu_usage', 50)
        cpu_health = max(0, 100 - (cpu * 1.5))
        factors['cpu_health'] = cpu_health
        
        # Memory health
        memory = metrics.get('memory_usage', 50)
        memory_health = max(0, 100 - (memory * 1.5))
        factors['memory_health'] = memory_health
        
        # Disk health
        disk = metrics.get('disk_usage', 50)
        disk_health = max(0, 100 - (disk * 1.2))
        factors['disk_health'] = disk_health
        
        # Error rate (0-100 where 100 = no errors)
        error_rate = metrics.get('error_rate', 0)
        error_health = max(0, 100 - (error_rate * 100))
        factors['error_health'] = error_health
        
        # Uptime (0-100 where 100 = 100% uptime)
        uptime = metrics.get('uptime_percent', 99.9)
        uptime_health = min(100, uptime)
        factors['uptime_health'] = uptime_health
        
        # Weighted average
        score = (
            cpu_health * 0.2 +
            memory_health * 0.2 +
            disk_health * 0.2 +
            error_health * 0.25 +
            uptime_health * 0.15
        )
        
        return DimensionScore(
            dimension=ScoreDimension.HEALTH,
            value=min(100, max(0, score)),
            weight=self.dimension_weights[ScoreDimension.HEALTH],
            factors=factors
        )
    
    def compute_relevance_score(self, entity: Dict[str, Any]) -> DimensionScore:
        """Compute relevance score based on usage and context."""
        factors = {}
        
        # Usage frequency (0-100)
        usage_count = entity.get('usage_count', 0)
        usage_score = min(100, usage_count / 10.0 * 100)
        factors['usage_frequency'] = usage_score
        
        # Recency (0-100, based on last access)
        last_access = entity.get('last_accessed_hours_ago', 24)
        recency_score = max(0, 100 - (last_access / 24 * 50))  # Decays over 24h
        factors['recency'] = recency_score
        
        # Context match (0-100, how well it matches search context)
        context_match = entity.get('context_match', 0.5)
        context_score = context_match * 100
        factors['context_match'] = context_score
        
        # Completeness (0-100, how much metadata/info available)
        completeness = entity.get('metadata_completeness', 0.5)
        completeness_score = completeness * 100
        factors['completeness'] = completeness_score
        
        # Weighted average
        score = (
            usage_score * 0.25 +
            recency_score * 0.25 +
            context_score * 0.30 +
            completeness_score * 0.20
        )
        
        return DimensionScore(
            dimension=ScoreDimension.RELEVANCE,
            value=min(100, max(0, score)),
            weight=self.dimension_weights[ScoreDimension.RELEVANCE],
            factors=factors
        )
    
    def compute_performance_score(self, metrics: Dict[str, Any]) -> DimensionScore:
        """Compute performance score."""
        factors = {}
        
        # Response time (0-100, where 100 = < 100ms)
        response_time = metrics.get('response_time_ms', 500)
        response_score = max(0, 100 - (response_time / 5))
        factors['response_time'] = response_score
        
        # Throughput (0-100, requests/sec normalized)
        throughput = metrics.get('throughput_rps', 100)
        throughput_score = min(100, (throughput / 1000) * 100)
        factors['throughput'] = throughput_score
        
        # Cache hit rate (0-100)
        cache_hit_rate = metrics.get('cache_hit_rate', 0.5)
        cache_score = cache_hit_rate * 100
        factors['cache_efficiency'] = cache_score
        
        # P99 latency (0-100)
        p99_latency = metrics.get('p99_latency_ms', 1000)
        p99_score = max(0, 100 - (p99_latency / 10))
        factors['p99_latency'] = p99_score
        
        # Weighted average
        score = (
            response_score * 0.30 +
            throughput_score * 0.25 +
            cache_score * 0.20 +
            p99_score * 0.25
        )
        
        return DimensionScore(
            dimension=ScoreDimension.PERFORMANCE,
            value=min(100, max(0, score)),
            weight=self.dimension_weights[ScoreDimension.PERFORMANCE],
            factors=factors
        )
    
    def compute_security_score(self, entity: Dict[str, Any]) -> DimensionScore:
        """Compute security score."""
        factors = {}
        
        # Authentication enabled (binary, 0 or 100)
        auth_enabled = entity.get('authentication_enabled', False)
        auth_score = 100 if auth_enabled else 20
        factors['authentication'] = auth_score
        
        # Encryption (binary, 0 or 100)
        encryption_enabled = entity.get('encryption_enabled', False)
        encryption_score = 100 if encryption_enabled else 30
        factors['encryption'] = encryption_score
        
        # Vulnerability count (0-100, normalized)
        vulnerabilities = entity.get('vulnerability_count', 0)
        vuln_score = max(0, 100 - (vulnerabilities * 10))
        factors['vulnerability_status'] = vuln_score
        
        # Compliance score (0-100)
        compliance = entity.get('compliance_score', 0.5)
        compliance_score = compliance * 100
        factors['compliance'] = compliance_score
        
        # Access control (0-100)
        access_control = entity.get('access_control_level', 0.5)
        access_score = access_control * 100
        factors['access_control'] = access_score
        
        # Weighted average
        score = (
            auth_score * 0.25 +
            encryption_score * 0.25 +
            vuln_score * 0.20 +
            compliance_score * 0.15 +
            access_score * 0.15
        )
        
        return DimensionScore(
            dimension=ScoreDimension.SECURITY,
            value=min(100, max(0, score)),
            weight=self.dimension_weights[ScoreDimension.SECURITY],
            factors=factors
        )
    
    def compute_reliability_score(self, metrics: Dict[str, Any]) -> DimensionScore:
        """Compute reliability score."""
        factors = {}
        
        # Mean time between failures (0-100)
        mtbf_hours = metrics.get('mean_time_between_failures_hours', 168)
        mtbf_score = min(100, (mtbf_hours / 168) * 100)  # Good = 1 week
        factors['mtbf'] = mtbf_score
        
        # Mean time to recovery (0-100, where 100 = < 5 min)
        mttr_minutes = metrics.get('mean_time_to_recovery_minutes', 30)
        mttr_score = max(0, 100 - (mttr_minutes / 0.5))  # Decays from 5 min
        factors['mttr'] = mttr_score
        
        # SLA compliance (0-100)
        sla_compliance = metrics.get('sla_compliance_percent', 99.0)
        sla_score = min(100, sla_compliance)
        factors['sla_compliance'] = sla_score
        
        # Incident count (0-100)
        incidents = metrics.get('incident_count_30d', 0)
        incident_score = max(0, 100 - (incidents * 5))
        factors['incident_rate'] = incident_score
        
        # Weighted average
        score = (
            mtbf_score * 0.25 +
            mttr_score * 0.25 +
            sla_score * 0.30 +
            incident_score * 0.20
        )
        
        return DimensionScore(
            dimension=ScoreDimension.RELIABILITY,
            value=min(100, max(0, score)),
            weight=self.dimension_weights[ScoreDimension.RELIABILITY],
            factors=factors
        )
    
    def compute_availability_score(self, metrics: Dict[str, Any]) -> DimensionScore:
        """Compute availability score."""
        factors = {}
        
        # Current status (0 or 100)
        is_available = metrics.get('is_available', True)
        status_score = 100 if is_available else 0
        factors['current_status'] = status_score
        
        # Uptime 24h (0-100)
        uptime_24h = metrics.get('uptime_24h_percent', 99.9)
        uptime_24_score = min(100, uptime_24h)
        factors['uptime_24h'] = uptime_24_score
        
        # Uptime 30d (0-100)
        uptime_30d = metrics.get('uptime_30d_percent', 99.0)
        uptime_30_score = min(100, uptime_30d)
        factors['uptime_30d'] = uptime_30_score
        
        # Redundancy (0-100, based on replica count)
        replicas = metrics.get('replica_count', 1)
        redundancy_score = min(100, (replicas - 1) * 50)  # 2+ replicas = 100
        factors['redundancy'] = redundancy_score
        
        # Weighted average
        score = (
            status_score * 0.30 +
            uptime_24_score * 0.25 +
            uptime_30_score * 0.25 +
            redundancy_score * 0.20
        )
        
        return DimensionScore(
            dimension=ScoreDimension.AVAILABILITY,
            value=min(100, max(0, score)),
            weight=self.dimension_weights[ScoreDimension.AVAILABILITY],
            factors=factors
        )
    
    def compute_composite_score(self, entity_id: str, entity_name: str, entity: Dict[str, Any]) -> CompositeScore:
        """Compute composite score across all dimensions."""
        
        # Extract metrics
        metrics = entity.get('metrics', {})
        
        # Compute dimension scores
        dimension_scores = {}
        dimension_scores['health'] = self.compute_health_score(metrics)
        dimension_scores['relevance'] = self.compute_relevance_score(entity)
        dimension_scores['performance'] = self.compute_performance_score(metrics)
        dimension_scores['security'] = self.compute_security_score(entity)
        dimension_scores['reliability'] = self.compute_reliability_score(metrics)
        dimension_scores['availability'] = self.compute_availability_score(metrics)
        
        # Compute weighted average
        overall_score = 0
        total_weight = 0
        
        for dim_name, dim_score in dimension_scores.items():
            overall_score += dim_score.value * dim_score.weight
            total_weight += dim_score.weight
        
        overall_score = overall_score / total_weight if total_weight > 0 else 0
        
        # Determine rating
        rating = 'poor'
        if overall_score >= self.thresholds['excellent']:
            rating = 'excellent'
        elif overall_score >= self.thresholds['good']:
            rating = 'good'
        elif overall_score >= self.thresholds['fair']:
            rating = 'fair'
        
        # Generate recommendations
        recommendations = self._generate_recommendations(dimension_scores, overall_score)
        
        # Determine trend
        trend = self._determine_trend(entity_id, overall_score)
        
        composite = CompositeScore(
            entity_id=entity_id,
            entity_name=entity_name,
            overall_score=min(100, max(0, overall_score)),
            dimension_scores=dimension_scores,
            trend=trend,
            rating=rating,
            recommendations=recommendations
        )
        
        # Store in history
        if entity_id not in self.score_history:
            self.score_history[entity_id] = []
        self.score_history[entity_id].append(composite)
        
        return composite
    
    def _generate_recommendations(self, dimension_scores: Dict[str, DimensionScore], overall_score: float) -> List[str]:
        """Generate recommendations based on scores."""
        recommendations = []
        
        # Find lowest scoring dimensions
        sorted_dims = sorted(dimension_scores.items(), key=lambda x: x[1].value)
        
        for dim_name, dim_score in sorted_dims[:2]:  # Top 2 lowest
            if dim_score.value < 70:
                if dim_name == 'health':
                    recommendations.append("Improve resource utilization (CPU/Memory/Disk)")
                elif dim_name == 'performance':
                    recommendations.append("Optimize response times and throughput")
                elif dim_name == 'security':
                    recommendations.append("Enhance security posture (auth, encryption, compliance)")
                elif dim_name == 'reliability':
                    recommendations.append("Reduce incident rate and improve MTTR")
                elif dim_name == 'availability':
                    recommendations.append("Increase redundancy and uptime")
        
        if overall_score < 60:
            recommendations.append("Critical: Prioritize improvements across all dimensions")
        
        return recommendations
    
    def _determine_trend(self, entity_id: str, current_score: float) -> str:
        """Determine trend based on score history."""
        if entity_id not in self.score_history or len(self.score_history[entity_id]) < 2:
            return "stable"
        
        history = self.score_history[entity_id]
        if len(history) < 2:
            return "stable"
        
        previous_score = history[-2].overall_score
        
        if current_score > previous_score + 5:
            return "improving"
        elif current_score < previous_score - 5:
            return "declining"
        else:
            return "stable"
    
    def get_score_distribution(self) -> Dict[str, Any]:
        """Get distribution of scores across all entities."""
        all_scores = []
        for scores in self.score_history.values():
            if scores:
                all_scores.append(scores[-1].overall_score)
        
        if not all_scores:
            return {}
        
        sorted_scores = sorted(all_scores)
        return {
            'min': min(all_scores),
            'max': max(all_scores),
            'mean': sum(all_scores) / len(all_scores),
            'median': sorted_scores[len(sorted_scores) // 2],
            'count': len(all_scores)
        }
