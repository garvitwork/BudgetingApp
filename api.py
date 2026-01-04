from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from functions import *

app = FastAPI(
    title="Personal Finance Manager API",
    description="Comprehensive personal finance management system with 12+ advanced features",
    version="1.0.0"
)

# CORS middleware for web access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class BudgetAllocationRequest(BaseModel):
    total_amount: float = Field(..., gt=0, description="Monthly income")
    savings_pct: float = Field(..., ge=0, le=100)
    investment_pct: float = Field(..., ge=0, le=100)
    personal_pct: float = Field(..., ge=0, le=100)
    misc_pct: float = Field(15, ge=0, le=100)

class GoalRequest(BaseModel):
    name: str
    target_amount: float = Field(..., gt=0)
    timeline_months: int = Field(..., gt=0)
    expected_return: float = Field(0, ge=0)

class CombinedGoalsRequest(BaseModel):
    total_income: float = Field(..., gt=0)
    allocation: Dict[str, float]
    savings_target: float = Field(..., gt=0)
    savings_months: int = Field(..., gt=0)
    investment_target: float = Field(..., gt=0)
    investment_months: int = Field(..., gt=0)
    annual_return: float = Field(..., ge=0)

class ExpenseForecastRequest(BaseModel):
    monthly_expenses_history: List[float] = Field(..., min_items=3)

class IncomeVolatilityRequest(BaseModel):
    income_history: List[float] = Field(..., min_items=2)

class InvestmentData(BaseModel):
    name: str
    purchase_value: float = Field(..., gt=0)
    current_value: float = Field(..., gt=0)

class TaxHarvestingRequest(BaseModel):
    investments: List[InvestmentData]

class OpportunityCostRequest(BaseModel):
    skipped_amount: float = Field(..., gt=0)
    months: int = Field(..., gt=0)
    annual_return_pct: float = Field(..., ge=0)

class AssetAllocationRequest(BaseModel):
    age: int = Field(..., ge=18)
    risk_tolerance: str = Field(..., pattern="^(conservative|moderate|aggressive)$")
    timeline_years: int = Field(..., gt=0)
    monthly_investment: Optional[float] = None

class DynamicReallocationRequest(BaseModel):
    allocation: Dict[str, float]
    actual_spending: Dict[str, float]
    months_tracked: int = Field(..., ge=2)

class MicroSavingsRequest(BaseModel):
    transactions: List[Dict[str, Any]]
    savings_threshold: float = Field(50, gt=0)

class StreakTrackingRequest(BaseModel):
    monthly_performance: List[Dict[str, bool]]
    goal_type: str = Field("budget_adherence")

class GoalConflictRequest(BaseModel):
    goals: List[GoalRequest] = Field(..., min_items=2)
    monthly_income: float = Field(..., gt=0)
    current_allocation: Dict[str, float]

class MarketConditions(BaseModel):
    status: str = Field(..., pattern="^(dip|correction|neutral|stable|peak|overvalued)$")
    volatility: str = Field(..., pattern="^(low|medium|high)$")

class MarketAdvisorRequest(BaseModel):
    current_market_conditions: MarketConditions
    investment_allocation: float = Field(..., gt=0)
    risk_tolerance: str = Field(..., pattern="^(conservative|moderate|aggressive)$")

class InflationAdjusterRequest(BaseModel):
    goals: List[GoalRequest]
    current_inflation_rate: float = Field(..., gt=0)

class BankFeedRequest(BaseModel):
    monthly_income: float = Field(..., gt=0)
    allocation: Dict[str, float]
    variance: float = Field(0.1, ge=0, le=1)

# ============================================================================
# CORE ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    return {
        "message": "Personal Finance Manager API",
        "version": "1.0.0",
        "features": [
            "Budget Allocation",
            "Goal Planning",
            "Expense Forecasting",
            "Income Volatility Buffer",
            "Tax-Loss Harvesting",
            "Opportunity Cost Calculator",
            "Asset Allocation Optimizer",
            "Dynamic Reallocation",
            "Micro-Savings Triggers",
            "Streak Tracking",
            "Goal Conflict Resolver",
            "Market-Aware Advisor",
            "Inflation Adjuster",
            "Bank Feed Integration"
        ]
    }

@app.post("/api/allocate-budget")
async def allocate_budget_endpoint(request: BudgetAllocationRequest):
    """Allocate monthly budget based on percentages"""
    total_pct = request.savings_pct + request.investment_pct + request.personal_pct + request.misc_pct
    if abs(total_pct - 100) > 0.01:
        raise HTTPException(400, f"Percentages must sum to 100%. Current sum: {total_pct}%")
    
    allocation = allocate_budget(
        request.total_amount,
        request.savings_pct,
        request.investment_pct,
        request.personal_pct,
        request.misc_pct
    )
    
    periods = {
        '1 Month': 1,
        '3 Months': 3,
        '6 Months': 6,
        '12 Months': 12,
        '24 Months': 24
    }
    projections = calculate_projections(allocation, periods)
    
    return {
        "allocation": allocation,
        "projections": projections,
        "total_allocated": sum(allocation.values())
    }

@app.post("/api/combined-goals")
async def combined_goals_endpoint(request: CombinedGoalsRequest):
    """Analyze both savings and investment goals together"""
    required_monthly_savings = savings_goal_calculator(
        request.savings_target,
        request.savings_months
    )
    
    required_monthly_investment = investment_goal_calculator(
        request.investment_target,
        request.investment_months,
        request.annual_return
    )
    
    savings_gap = request.allocation['savings'] - required_monthly_savings
    investment_gap = request.allocation['investments'] - required_monthly_investment
    
    total_shortfall = 0
    if savings_gap < 0:
        total_shortfall += abs(savings_gap)
    if investment_gap < 0:
        total_shortfall += abs(investment_gap)
    
    new_allocation = None
    if total_shortfall > 0:
        new_allocation = create_unified_reallocation_plan(
            request.allocation.copy(),
            abs(savings_gap) if savings_gap < 0 else 0,
            abs(investment_gap) if investment_gap < 0 else 0,
            request.total_income
        )
    
    # Generate AI analysis
    analysis = generate_ai_analysis(
        request.total_income,
        request.allocation,
        savings_gap,
        investment_gap
    )
    
    return {
        "required_monthly_savings": required_monthly_savings,
        "required_monthly_investment": required_monthly_investment,
        "current_allocation": request.allocation,  # ← ADD THIS LINE
        "savings_gap": savings_gap,
        "investment_gap": investment_gap,
        "total_shortfall": total_shortfall,
        "goals_met": total_shortfall == 0,
        "new_allocation": new_allocation,
        "ai_analysis": analysis
    }

# ============================================================================
# ADVANCED ANALYTICS ENDPOINTS
# ============================================================================

@app.post("/api/expense-forecast")
async def expense_forecast_endpoint(request: ExpenseForecastRequest):
    """Predict irregular expenses 2-3 months ahead"""
    predictions = expense_forecasting(request.monthly_expenses_history)
    
    if not predictions:
        raise HTTPException(400, "Need at least 3 months of expense data")
    
    return {"predictions": predictions}

@app.post("/api/income-volatility")
async def income_volatility_endpoint(request: IncomeVolatilityRequest):
    """Calculate smoothed budget based on income average"""
    buffer_data = income_volatility_buffer(request.income_history)
    
    if not buffer_data:
        raise HTTPException(400, "Need at least 2 months of income data")
    
    return buffer_data

@app.post("/api/tax-harvesting")
async def tax_harvesting_endpoint(request: TaxHarvestingRequest):
    """Flag underperforming investments for tax optimization"""
    investments_data = [inv.dict() for inv in request.investments]
    opportunities = tax_loss_harvesting_tracker(investments_data)
    
    return {
        "opportunities": opportunities if opportunities else [],
        "has_opportunities": opportunities is not None
    }

@app.post("/api/opportunity-cost")
async def opportunity_cost_endpoint(request: OpportunityCostRequest):
    """Calculate future value lost by skipping investment"""
    cost_data = opportunity_cost_calculator(
        request.skipped_amount,
        request.months,
        request.annual_return_pct
    )
    
    return cost_data

# ============================================================================
# BEHAVIORAL & OPTIMIZATION ENDPOINTS
# ============================================================================

@app.post("/api/asset-allocation")
async def asset_allocation_endpoint(request: AssetAllocationRequest):
    """Suggest optimal stock/bond/cash allocation"""
    allocation_data = asset_allocation_optimizer(
        request.age,
        request.risk_tolerance,
        request.timeline_years
    )
    
    result = {"allocation": allocation_data}
    
    if request.monthly_investment and request.monthly_investment > 0:
        result["monthly_breakdown"] = {
            "stocks": (allocation_data['stocks'] / 100) * request.monthly_investment,
            "bonds": (allocation_data['bonds'] / 100) * request.monthly_investment,
            "cash": (allocation_data['cash'] / 100) * request.monthly_investment
        }
    
    return result

@app.post("/api/dynamic-reallocation")
async def dynamic_reallocation_endpoint(request: DynamicReallocationRequest):
    """Suggest fund reallocation based on spending patterns"""
    suggestions = dynamic_reallocation_suggestions(
        request.allocation,
        request.actual_spending,
        request.months_tracked
    )
    
    return {
        "suggestions": suggestions if suggestions else [],
        "has_suggestions": suggestions is not None
    }

@app.post("/api/micro-savings")
async def micro_savings_endpoint(request: MicroSavingsRequest):
    """Convert small budget wins into automatic savings"""
    micro_data = micro_savings_triggers(
        request.transactions,
        request.savings_threshold
    )
    
    return {
        "data": micro_data if micro_data else {},
        "has_savings": micro_data is not None
    }

@app.post("/api/streak-tracking")
async def streak_tracking_endpoint(request: StreakTrackingRequest):
    """Track financial discipline streaks"""
    streak_data = streak_tracking(
        request.monthly_performance,
        request.goal_type
    )
    
    if not streak_data:
        raise HTTPException(400, "Need at least 1 month of performance data")
    
    return streak_data

# ============================================================================
# STRATEGIC INTELLIGENCE ENDPOINTS
# ============================================================================

@app.post("/api/goal-conflict-resolver")
async def goal_conflict_resolver_endpoint(request: GoalConflictRequest):
    """Prioritize and resolve competing financial goals"""
    goals_list = []
    
    for goal in request.goals:
        # Calculate monthly required
        if goal.expected_return > 0:
            r = (goal.expected_return / 100) / 12
            monthly_req = goal.target_amount * r / (((1 + r) ** goal.timeline_months) - 1)
        else:
            monthly_req = goal.target_amount / goal.timeline_months
        
        goals_list.append({
            'name': goal.name,
            'target_amount': goal.target_amount,
            'timeline_months': goal.timeline_months,
            'deadline_months': goal.timeline_months,
            'expected_return': goal.expected_return,
            'monthly_required': monthly_req
        })
    
    scored_goals = goal_conflict_resolver(
        goals_list,
        request.monthly_income,
        request.current_allocation
    )
    
    if not scored_goals:
        raise HTTPException(400, "Need at least 2 goals for conflict resolution")
    
    return {
        "scored_goals": scored_goals,
        "top_priority": scored_goals[0] if scored_goals else None,
        "total_goals": len(scored_goals)
    }

@app.post("/api/market-advisor")
async def market_advisor_endpoint(request: MarketAdvisorRequest):
    """Provide strategic investment advice based on market conditions"""
    market_conditions_dict = request.current_market_conditions.dict()
    
    advisor_data = market_aware_advisor(
        market_conditions_dict,
        request.investment_allocation,
        request.risk_tolerance
    )
    
    if not advisor_data:
        raise HTTPException(400, "Market data required")
    
    return advisor_data

@app.post("/api/inflation-adjuster")
async def inflation_adjuster_endpoint(request: InflationAdjusterRequest):
    """Auto-adjust goal targets based on inflation"""
    goals_list = []
    
    for goal in request.goals:
        # Calculate monthly required
        if goal.expected_return > 0:
            r = (goal.expected_return / 100) / 12
            monthly_req = goal.target_amount * r / (((1 + r) ** goal.timeline_months) - 1)
        else:
            monthly_req = goal.target_amount / goal.timeline_months
        
        goals_list.append({
            'name': goal.name,
            'target_amount': goal.target_amount,
            'timeline_months': goal.timeline_months,
            'expected_return': goal.expected_return,
            'monthly_required': monthly_req
        })
    
    adjusted_goals = inflation_adjuster(goals_list, request.current_inflation_rate)
    
    if not adjusted_goals:
        raise HTTPException(400, "No goals to adjust for inflation")
    
    total_impact = sum(g['inflation_impact'] for g in adjusted_goals)
    total_monthly_increase = sum(g['monthly_increase'] for g in adjusted_goals)
    
    return {
        "adjusted_goals": adjusted_goals,
        "total_impact": total_impact,
        "total_monthly_increase": total_monthly_increase,
        "inflation_rate": request.current_inflation_rate
    }

@app.post("/api/bank-feed-simulator")
async def bank_feed_endpoint(request: BankFeedRequest):
    """Simulate bank transactions and auto-categorize them"""
    feed_data = bank_feed_simulator(
        request.monthly_income,
        request.allocation,
        request.variance
    )
    
    return feed_data

# ============================================================================
# UTILITY ENDPOINTS
# ============================================================================

@app.post("/api/savings-goal")
async def savings_goal_endpoint(target_amount: float, months: int):
    """Calculate required monthly savings to reach target"""
    if target_amount <= 0 or months <= 0:
        raise HTTPException(400, "Target amount and months must be positive")
    
    monthly_required = savings_goal_calculator(target_amount, months)
    
    return {
        "target_amount": target_amount,
        "months": months,
        "monthly_required": monthly_required
    }

@app.post("/api/investment-goal")
async def investment_goal_endpoint(
    target_amount: float,
    months: int,
    annual_return_pct: float
):
    """Calculate required monthly investment with compound returns"""
    if target_amount <= 0 or months <= 0:
        raise HTTPException(400, "Target amount and months must be positive")
    
    monthly_required = investment_goal_calculator(
        target_amount,
        months,
        annual_return_pct
    )
    
    return {
        "target_amount": target_amount,
        "months": months,
        "annual_return_pct": annual_return_pct,
        "monthly_required": monthly_required
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "Personal Finance Manager API",
        "version": "1.0.0"
    }

# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)