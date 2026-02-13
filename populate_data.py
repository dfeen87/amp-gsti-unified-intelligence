"""
AMP-GSTI Automated Data Populator
==================================
Fetches real-time market data and populates the API with:
- Live gold/silver prices from financial APIs
- Market sentiment indicators (VIX)
- Sample candidate data with realistic SBTs
- Continuous market updates

Usage:
    python populate_data.py --mode continuous
    python populate_data.py --mode once
    python populate_data.py --populate-candidates 50
"""

import argparse
import logging
import random
import secrets
import time
from datetime import datetime, timedelta
from typing import Dict, List

import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURATION
# ============================================================================

API_BASE = "http://localhost:8000"

# Free API endpoints for real market data
GOLD_SILVER_API = "https://api.metals.live/v1/spot"  # Free, no key needed
ALTERNATIVE_METALS_API = "https://www.goldapi.io/api"  # Requires free API key
VIX_PROXY_API = "https://query1.finance.yahoo.com/v8/finance/chart/%5EVIX"

# Sample data pools for realistic candidate generation
SKILLS = [
    "Python Mastery", "JavaScript Expert", "Rust Programming", "Go Development",
    "Machine Learning", "Deep Learning", "Data Science", "Cloud Architecture",
    "Kubernetes", "Docker", "DevOps", "CI/CD", "System Design",
    "Blockchain Development", "Smart Contracts", "Web3", "DeFi",
    "Frontend Development", "Backend Development", "Full Stack",
    "Mobile Development", "React Native", "iOS Development", "Android Development",
    "Database Design", "SQL Optimization", "NoSQL", "PostgreSQL", "MongoDB",
    "API Design", "Microservices", "GraphQL", "REST APIs",
    "Security Engineering", "Cryptography", "Zero-Knowledge Proofs",
    "Product Management", "Agile Methodology", "Scrum Master",
    "Technical Writing", "Documentation", "Code Review"
]

CHARACTER_TRAITS = [
    "Leadership", "Team Player", "Mentor", "Problem Solver",
    "Creative Thinker", "Analytical Mind", "Strategic Vision",
    "Adaptability", "Resilience", "Emotional Intelligence",
    "Communication Skills", "Conflict Resolution", "Initiative",
    "Accountability", "Integrity", "Empathy", "Collaboration",
    "Critical Thinking", "Innovation", "Continuous Learner"
]

LOYALTY_MARKERS = [
    "5 Year Tenure", "10 Year Tenure", "Long-term Commitment",
    "Company Advocate", "Culture Champion", "Retention Award",
    "Loyalty Recognition", "Veteran Status", "Senior Member",
    "Legacy Builder", "Institutional Knowledge"
]

CERTIFICATIONS = [
    "AWS Certified Solutions Architect", "Google Cloud Professional",
    "Microsoft Azure Expert", "Certified Kubernetes Administrator",
    "CISSP", "CEH", "PMP", "Scrum Master Certification",
    "Machine Learning Specialization", "Deep Learning Nanodegree",
    "Blockchain Certification", "Security+", "Network+",
    "Docker Certified Associate", "Terraform Associate"
]

PROJECT_TOKENS = [
    "Led $10M Project", "Startup Founder", "Open Source Contributor",
    "Product Launch Success", "Innovation Award Winner",
    "Patent Holder", "Published Researcher", "Conference Speaker",
    "Hackathon Winner", "Technical Mentor Program"
]

ISSUERS = [
    "Tech Certification Board", "Global Skills Authority", "Industry Consortium",
    "Professional Standards Committee", "Blockchain Credentialing Network",
    "Corporate HR Department", "Independent Verifier", "Peer Review Board",
    "Academic Institution", "Professional Association"
]

# ============================================================================
# MARKET DATA FETCHERS
# ============================================================================

class MarketDataFetcher:
    """Fetch real-time market data from various sources"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AMP-GSTI-Data-Populator/1.0'
        })
    
    def fetch_gold_silver_prices(self) -> Dict:
        """
        Fetch live gold and silver prices
        Falls back to realistic simulated data if APIs fail
        """
        try:
            # Try metals.live API (free, no key)
            response = self.session.get(GOLD_SILVER_API, timeout=5)
            if response.status_code == 200:
                data = response.json()
                gold_price = float(data.get('gold', 2500))
                silver_price = float(data.get('silver', 25))
                
                # Validate prices are positive
                if gold_price <= 0 or silver_price <= 0:
                    raise ValueError(f"Invalid prices: gold={gold_price}, silver={silver_price}")
                
                return {
                    'gold_price': gold_price,
                    'silver_price': silver_price,
                    'source': 'metals.live',
                    'timestamp': datetime.utcnow().isoformat()
                }
        except Exception as e:
            logger.warning(f"Failed to fetch from metals.live: {e}")
        
        # Fallback: Generate realistic prices with slight random walk
        base_gold = 2450 + random.uniform(-100, 100)
        base_silver = 24 + random.uniform(-2, 2)
        
        return {
            'gold_price': round(base_gold, 2),
            'silver_price': round(base_silver, 2),
            'source': 'simulated',
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def fetch_vix(self) -> float:
        """
        Fetch VIX (market volatility) or simulate
        """
        try:
            # Try Yahoo Finance API
            response = self.session.get(VIX_PROXY_API, timeout=5)
            if response.status_code == 200:
                data = response.json()
                vix = data['chart']['result'][0]['meta']['regularMarketPrice']
                return float(vix)
        except Exception as e:
            logger.warning(f"Failed to fetch VIX: {e}")
        
        # Fallback: Simulate VIX between 15-35 with realistic distribution
        return round(random.gauss(20, 5), 2)
    
    def generate_goodwill_metrics(self) -> Dict:
        """
        Generate realistic goodwill metrics
        In production, these would come from company surveys, NPS, employee engagement, etc.
        """
        # Simulate realistic business metrics with some correlation
        base_health = random.uniform(0.7, 0.9)
        
        return {
            'CR': round(base_health + random.uniform(-0.1, 0.1), 2),  # Customer Retention
            'ES': round(base_health + random.uniform(-0.15, 0.1), 2),  # Employee Satisfaction
            'BT': round(base_health + random.uniform(-0.1, 0.1), 2),  # Brand Trust
            'RG': round(1.0 + random.uniform(-0.05, 0.15), 2),  # Revenue Growth
            'NCB': round(random.uniform(0.05, 0.15), 2),  # Net Customer Backlash
            'CS': round(base_health + random.uniform(0, 0.15), 2),  # Customer Satisfaction
            'BR': round(base_health + random.uniform(-0.05, 0.1), 2),  # Brand Reputation
            'CA': round(base_health + random.uniform(-0.15, 0.05), 2),  # Customer Advocacy
            'SS': round(base_health + random.uniform(-0.1, 0.15), 2),  # Service Speed
            'NCB_consumer': round(random.uniform(0.02, 0.08), 2),  # Consumer Backlash
        }
    
    def detect_ma_surges(self) -> bool:
        """
        Detect M&A activity surges
        In production, this would query M&A databases or news APIs
        """
        # Simulate: 20% chance of M&A surge
        return random.random() < 0.2

# ============================================================================
# CANDIDATE GENERATOR
# ============================================================================

class CandidateGenerator:
    """Generate realistic candidate profiles"""
    
    @staticmethod
    def generate_wallet_address() -> str:
        """Generate a realistic-looking Ethereum wallet address"""
        return "0x" + secrets.token_hex(20)
    
    @staticmethod
    def generate_tokens(num_tokens: int = None) -> List[Dict]:
        """Generate realistic SBT tokens for a candidate"""
        if num_tokens is None:
            num_tokens = random.randint(3, 12)
        
        tokens = []
        
        # Ensure at least one of each critical type
        token_types = [
            ('skill', SKILLS, 2, 5),
            ('character', CHARACTER_TRAITS, 1, 3),
            ('certification', CERTIFICATIONS, 0, 2),
            ('project', PROJECT_TOKENS, 0, 2),
            ('loyalty', LOYALTY_MARKERS, 0, 1)
        ]
        
        for token_type, pool, min_count, max_count in token_types:
            count = random.randint(min_count, min(max_count, num_tokens))
            selected = random.sample(pool, min(count, len(pool)))
            
            for name in selected:
                tokens.append({
                    'type': token_type,
                    'name': name,
                    'issuer': random.choice(ISSUERS),
                    'issue_date': (datetime.now() - timedelta(days=random.randint(30, 1825))).strftime('%Y-%m'),
                    'verification_hash': '0x' + secrets.token_hex(32)
                })
        
        return tokens[:num_tokens]
    
    @staticmethod
    def generate_candidate() -> Dict:
        """Generate a complete candidate profile"""
        # Experience affects score
        years_exp = random.randint(1, 20)
        
        # Base score correlated with experience but with variance
        base_score = min(100, max(40, 
            60 + (years_exp * 1.5) + random.gauss(0, 10)
        ))
        
        return {
            'wallet_address': CandidateGenerator.generate_wallet_address(),
            'tokens': CandidateGenerator.generate_tokens(),
            'years_experience': years_exp,
            'base_predictive_score': round(base_score, 2)
        }

# ============================================================================
# API CLIENT
# ============================================================================

class AMPGSTIClient:
    """Client for interacting with AMP-GSTI API"""
    
    def __init__(self, base_url: str = API_BASE):
        self.base_url = base_url
        self.session = requests.Session()
    
    def update_market_data(self, market_data: Dict, goodwill: Dict, vix: float, ma_surges: bool):
        """Update GSTI market intelligence"""
        params = {
            'gold_price': market_data['gold_price'],
            'silver_price': market_data['silver_price'],
            'VIX': vix,
            'M_A_Surges': ma_surges,
            **goodwill
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/market/gsti/update",
                params=params
            )
            response.raise_for_status()
            logger.info(f"Market data updated: GSR={market_data['gold_price']/market_data['silver_price']:.2f}, VIX={vix}")
            return response.json()
        except Exception as e:
            logger.error(f"Failed to update market data: {e}")
            return None
    
    def register_candidate(self, candidate: Dict):
        """Register a candidate"""
        try:
            response = self.session.post(
                f"{self.base_url}/candidates/register",
                json=candidate
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if "already registered" in str(e):
                logger.debug("Candidate already registered, skipping")
                return None  # Skip duplicates
            logger.error(f"Failed to register candidate: {e}")
            return None
    
    def get_system_status(self):
        """Get system status"""
        try:
            response = self.session.get(f"{self.base_url}/system/status")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get system status: {e}")
            return None
    
    def reset_system(self):
        """Reset system (use with caution)"""
        try:
            response = self.session.post(
                f"{self.base_url}/system/reset",
                params={'confirm': True}
            )
            response.raise_for_status()
            logger.info("System reset successful")
            return response.json()
        except Exception as e:
            logger.error(f"Failed to reset system: {e}")
            return None

# ============================================================================
# MAIN POPULATOR
# ============================================================================

class DataPopulator:
    """Main data population orchestrator"""
    
    def __init__(self, api_base: str = API_BASE):
        self.fetcher = MarketDataFetcher()
        self.generator = CandidateGenerator()
        self.client = AMPGSTIClient(api_base)
    
    def populate_candidates(self, count: int = 50):
        """Populate database with candidates"""
        print(f"\n{'='*60}")
        print(f"POPULATING {count} CANDIDATES")
        print(f"{'='*60}\n")
        
        success_count = 0
        for i in range(count):
            candidate = self.generator.generate_candidate()
            result = self.client.register_candidate(candidate)
            
            if result:
                success_count += 1
                print(f"✓ Candidate {i+1}/{count}: {candidate['wallet_address'][:10]}... "
                      f"({candidate['years_experience']} yrs, {len(candidate['tokens'])} tokens, "
                      f"score: {candidate['base_predictive_score']:.1f})")
            
            # Brief pause to avoid overwhelming the API
            time.sleep(0.1)
        
        print(f"\n✓ Successfully registered {success_count}/{count} candidates\n")
    
    def update_market_once(self):
        """Update market data once"""
        print(f"\n{'='*60}")
        print("UPDATING MARKET DATA")
        print(f"{'='*60}\n")
        
        # Fetch real data
        metals = self.fetcher.fetch_gold_silver_prices()
        vix = self.fetcher.fetch_vix()
        goodwill = self.fetcher.generate_goodwill_metrics()
        ma_surges = self.fetcher.detect_ma_surges()
        
        print(f"Gold: ${metals['gold_price']:.2f}")
        print(f"Silver: ${metals['silver_price']:.2f}")
        print(f"GSR: {metals['gold_price']/metals['silver_price']:.2f}")
        print(f"VIX: {vix}")
        print(f"M&A Surges: {ma_surges}")
        print(f"Data Source: {metals['source']}\n")
        
        # Update API
        result = self.client.update_market_data(metals, goodwill, vix, ma_surges)
        
        if result:
            regime = result.get('data', {}).get('market_regime', 'unknown')
            gsti = result.get('data', {}).get('gsti_score', 0)
            print(f"\n✓ Market regime: {regime.upper()}")
            print(f"✓ GSTI Score: {gsti:.4f}\n")
    
    def run_continuous(self, interval: int = 300):
        """Continuously update market data"""
        print(f"\n{'='*60}")
        print("CONTINUOUS MARKET UPDATE MODE")
        print(f"Updating every {interval} seconds (Ctrl+C to stop)")
        print(f"{'='*60}\n")
        
        try:
            while True:
                self.update_market_once()
                
                # Show countdown
                print(f"Next update in {interval} seconds...")
                time.sleep(interval)
        
        except KeyboardInterrupt:
            print("\n\n✓ Stopped continuous updates\n")
    
    def show_status(self):
        """Show system status"""
        status = self.client.get_system_status()
        
        if status:
            print(f"\n{'='*60}")
            print("SYSTEM STATUS")
            print(f"{'='*60}\n")
            
            components = status.get('components', {})
            
            # GSTI Engine
            gsti = components.get('gsti_engine', {})
            print("GSTI Engine:")
            print(f"  - Historical data points: {gsti.get('historical_data_points', 0)}")
            print(f"  - Goodwill weight: {gsti.get('current_weights', {}).get('w_goodwill', 0)}")
            print(f"  - GSR weight: {gsti.get('current_weights', {}).get('w_gsr', 0)}")
            
            # AMP Engine
            amp = components.get('amp_engine', {})
            print("\nAMP Engine:")
            print(f"  - Candidates registered: {amp.get('candidates_registered', 0)}")
            
            # Market Intelligence
            market = components.get('market_intelligence', {})
            print("\nMarket Intelligence:")
            print(f"  - GSTI data available: {market.get('gsti_data_available', False)}")
            print(f"  - Current regime: {market.get('current_regime', 'unknown').upper()}")
            
            print(f"\nTimestamp: {status.get('timestamp', 'N/A')}\n")

# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='AMP-GSTI Automated Data Populator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Populate 50 candidates
  python populate_data.py --populate-candidates 50
  
  # Update market data once
  python populate_data.py --mode once
  
  # Continuous updates every 5 minutes
  python populate_data.py --mode continuous --interval 300
  
  # Full setup: reset, populate, then continuous updates
  python populate_data.py --reset --populate-candidates 100 --mode continuous
        """
    )
    
    parser.add_argument(
        '--mode',
        choices=['once', 'continuous'],
        default='once',
        help='Update mode: once or continuous'
    )
    
    parser.add_argument(
        '--interval',
        type=int,
        default=300,
        help='Update interval in seconds for continuous mode (default: 300)'
    )
    
    parser.add_argument(
        '--populate-candidates',
        type=int,
        metavar='COUNT',
        help='Populate N candidates before starting updates'
    )
    
    parser.add_argument(
        '--reset',
        action='store_true',
        help='Reset system before populating (CAUTION: deletes all data)'
    )
    
    parser.add_argument(
        '--status',
        action='store_true',
        help='Show system status and exit'
    )
    
    parser.add_argument(
        '--api-base',
        default='http://localhost:8000',
        help='API base URL (default: http://localhost:8000)'
    )
    
    args = parser.parse_args()
    
    # Update API base if provided
    api_base = args.api_base
    
    populator = DataPopulator(api_base=api_base)
    
    # Status check
    if args.status:
        populator.show_status()
        return
    
    # Reset if requested
    if args.reset:
        confirm = input("⚠️  WARNING: This will delete all data. Type 'yes' to confirm: ")
        if confirm.lower() == 'yes':
            populator.client.reset_system()
        else:
            print("Reset cancelled")
            return
    
    # Populate candidates if requested
    if args.populate_candidates:
        populator.populate_candidates(args.populate_candidates)
    
    # Update market data
    if args.mode == 'once':
        populator.update_market_once()
        populator.show_status()
    else:
        populator.run_continuous(args.interval)

if __name__ == '__main__':
    main()
