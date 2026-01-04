def allocate_budget(total_amount, savings_pct, investment_pct, personal_pct, misc_pct=15):
    """Allocate monthly budget based on percentages"""
    return {
        'savings': total_amount * (savings_pct / 100),
        'investments': total_amount * (investment_pct / 100),
        'personal': total_amount * (personal_pct / 100),
        'misc': total_amount * (misc_pct / 100)
    }

def calculate_projections(allocation, periods):
    """Calculate projections for multiple time periods"""
    projections = {}
    for period_name, months in periods.items():
        projections[period_name] = {
            category: amount * months 
            for category, amount in allocation.items()
        }
    return projections

def savings_goal_calculator(target_amount, months):
    """Calculate required monthly savings to reach target"""
    return target_amount / months

def investment_goal_calculator(target_amount, months, annual_return_pct):
    """Calculate required monthly investment with compound returns"""
    r = (annual_return_pct / 100) / 12  # monthly return
    n = months
    
    if r == 0:
        return target_amount / n
    
    # PMT = FV * r / ((1 + r)^n - 1)
    monthly_payment = target_amount * r / (((1 + r) ** n) - 1)
    return monthly_payment

def display_allocation_table(projections):
    """Display allocations in table format"""
    periods = list(projections.keys())
    categories = list(projections[periods[0]].keys())
    
    # Header
    print("\n" + "="*80)
    print(f"{'Category':<15}", end="")
    for period in periods:
        print(f"{period:>12}", end="")
    print("\n" + "="*80)
    
    # Rows
    for category in categories:
        print(f"{category.capitalize():<15}", end="")
        for period in periods:
            amount = projections[period][category]
            print(f"₹{amount:>10,.0f}", end="")
        print()
    
    # Total row
    print("-"*80)
    print(f"{'Total':<15}", end="")
    for period in periods:
        total = sum(projections[period].values())
        print(f"₹{total:>10,.0f}", end="")
    print("\n" + "="*80)

def get_float_input(prompt, min_val=0):
    """Get validated float input from user"""
    while True:
        try:
            value = float(input(prompt))
            if value < min_val:
                print(f"Value must be >= {min_val}")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_int_input(prompt, min_val=1):
    """Get validated integer input from user"""
    while True:
        try:
            value = int(input(prompt))
            if value < min_val:
                print(f"Value must be >= {min_val}")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a whole number.")

def display_combined_goal_analysis(savings_required, investment_required, allocation, total_income):
    """Analyze both goals together and provide unified reallocation plan"""
    print(f"\n{'='*80}")
    print(" "*25 + "COMBINED GOAL ANALYSIS")
    print(f"{'='*80}")
    
    print(f"\n{'Goal Type':<20} {'Required Monthly':<20} {'Current Allocation':<20} {'Gap':<15}")
    print("-" * 80)
    
    savings_gap = allocation['savings'] - savings_required
    investment_gap = allocation['investments'] - investment_required
    
    # Display savings
    gap_str = f"₹{savings_gap:,.0f}" if savings_gap >= 0 else f"-₹{abs(savings_gap):,.0f}"
    status = "✓" if savings_gap >= 0 else "✗"
    print(f"{status} Savings{'':<12} ₹{savings_required:<18,.2f} ₹{allocation['savings']:<18,.2f} {gap_str:<15}")
    
    # Display investments
    gap_str = f"₹{investment_gap:,.0f}" if investment_gap >= 0 else f"-₹{abs(investment_gap):,.0f}"
    status = "✓" if investment_gap >= 0 else "✗"
    print(f"{status} Investments{'':<8} ₹{investment_required:<18,.2f} ₹{allocation['investments']:<18,.2f} {gap_str:<15}")
    
    print("-" * 80)
    
    # Calculate total shortfall
    total_shortfall = 0
    if savings_gap < 0:
        total_shortfall += abs(savings_gap)
    if investment_gap < 0:
        total_shortfall += abs(investment_gap)
    
    if total_shortfall == 0:
        print("\n✓ Your current allocations meet both goals!")
        print("  Consider increasing targets or building additional financial cushion.")
    else:
        print(f"\n✗ Total Shortfall: ₹{total_shortfall:,.2f}/month")
        print("\n📋 UNIFIED REALLOCATION PLAN TO MEET BOTH GOALS:")
        
        # Create unified reallocation plan
        new_allocation = create_unified_reallocation_plan(
            allocation.copy(), 
            abs(savings_gap) if savings_gap < 0 else 0,
            abs(investment_gap) if investment_gap < 0 else 0,
            total_income
        )
        
        if new_allocation:
            print(f"\n{'Category':<15} {'Current':<15} {'Suggested':<15} {'Change':<15}")
            print("-" * 60)
            
            for category in allocation.keys():
                current = allocation[category]
                suggested = new_allocation[category]
                change = suggested - current
                change_str = f"+₹{change:,.0f}" if change > 0 else f"-₹{abs(change):,.0f}" if change < 0 else "₹0"
                
                print(f"{category.capitalize():<15} ₹{current:<14,.0f} ₹{suggested:<14,.0f} {change_str:<15}")
            
            print("-" * 60)
            print(f"{'Total':<15} ₹{sum(allocation.values()):<14,.0f} ₹{sum(new_allocation.values()):<14,.0f}")
            
            # Verify goals are met
            print(f"\n✓ New savings allocation: ₹{new_allocation['savings']:,.0f} (Required: ₹{savings_required:,.0f})")
            print(f"✓ New investment allocation: ₹{new_allocation['investments']:,.0f} (Required: ₹{investment_required:,.0f})")
            print("\n💡 Apply this plan to meet both goals while keeping total budget same.")
        else:
            print("\n⚠️  Cannot reallocate - discretionary spending already at minimum (5% each).")
            print(f"   Total shortfall of ₹{total_shortfall:,.0f}/month cannot be covered.")
            print(f"   Options:")
            print(f"   1. Increase monthly income")
            print(f"   2. Extend goal timelines")
            print(f"   3. Reduce target amounts")
    
    print(f"{'='*80}\n")
    
    return savings_gap, investment_gap

def create_unified_reallocation_plan(allocation, savings_shortfall, investment_shortfall, total_income):
    """Create unified plan to reallocate budget for both goals"""
    new_allocation = allocation.copy()
    total_shortfall = savings_shortfall + investment_shortfall
    remaining_shortfall = total_shortfall
    
    # Priority order for reducing: misc > personal
    reduction_priority = ['misc', 'personal']
    
    for category in reduction_priority:
        if remaining_shortfall <= 0:
            break
        
        # Keep minimum 5% in each category
        min_amount = total_income * 0.05
        available = max(0, allocation[category] - min_amount)
        
        reduction = min(available, remaining_shortfall)
        
        if reduction > 0:
            new_allocation[category] -= reduction
            remaining_shortfall -= reduction
    
    # Distribute freed amount to savings and investments proportionally
    if remaining_shortfall < total_shortfall:
        freed_amount = total_shortfall - remaining_shortfall
        
        # Add to savings first, then investments
        if savings_shortfall > 0:
            amount_to_savings = min(savings_shortfall, freed_amount)
            new_allocation['savings'] += amount_to_savings
            freed_amount -= amount_to_savings
        
        if investment_shortfall > 0 and freed_amount > 0:
            amount_to_investments = min(investment_shortfall, freed_amount)
            new_allocation['investments'] += amount_to_investments
        
        return new_allocation
    
    return None

def generate_ai_analysis(total_income, allocation, savings_gap, investment_gap):
    """Generate AI-powered financial analysis and recommendations"""
    
    # Calculate key metrics
    total_allocated = sum(allocation.values())
    savings_ratio = (allocation['savings'] / total_income) * 100
    investment_ratio = (allocation['investments'] / total_income) * 100
    discretionary = allocation['personal'] + allocation['misc']
    discretionary_ratio = (discretionary / total_income) * 100
    
    analysis = {
        'allocation_health': analyze_allocation_health(savings_ratio, investment_ratio, discretionary_ratio),
        'recommendations': [],
        'identified_leaks': [],
        'priority_actions': []
    }
    
    # Analyze savings gap
    if savings_gap < 0:
        analysis['identified_leaks'].append(f"Savings shortfall of ₹{abs(savings_gap):,.0f}/month")
        if discretionary_ratio > 40:
            analysis['recommendations'].append(
                f"Reduce discretionary spending (currently {discretionary_ratio:.1f}%) by ₹{abs(savings_gap):,.0f}"
            )
            analysis['priority_actions'].append("Cut personal/misc expenses")
    
    # Analyze investment gap
    if investment_gap < 0:
        analysis['identified_leaks'].append(f"Investment shortfall of ₹{abs(investment_gap):,.0f}/month")
        if allocation['misc'] > total_income * 0.15:
            potential_redirect = allocation['misc'] - (total_income * 0.15)
            analysis['recommendations'].append(
                f"Redirect ₹{potential_redirect:,.0f} from misc to investments"
            )
            analysis['priority_actions'].append("Optimize misc expenses")
    
    # General recommendations
    if savings_ratio < 20:
        analysis['recommendations'].append(
            f"Increase savings to at least 20% (currently {savings_ratio:.1f}%)"
        )
        analysis['priority_actions'].append("Boost emergency fund")
    
    if investment_ratio < 15:
        analysis['recommendations'].append(
            f"Aim for 15-20% investment allocation (currently {investment_ratio:.1f}%)"
        )
        analysis['priority_actions'].append("Increase wealth building")
    
    if discretionary_ratio > 50:
        analysis['identified_leaks'].append(
            f"High discretionary spending: {discretionary_ratio:.1f}% of income"
        )
        analysis['recommendations'].append("Review personal expenses for optimization opportunities")
    
    # Positive feedback
    if savings_gap >= 0 and investment_gap >= 0:
        analysis['recommendations'].append("✓ Your allocations meet your goals. Consider increasing targets.")
    
    if savings_ratio >= 20 and investment_ratio >= 15:
        analysis['recommendations'].append("✓ Strong financial foundation. Stay consistent.")
    
    return analysis

def analyze_allocation_health(savings_ratio, investment_ratio, discretionary_ratio):
    """Determine overall health score"""
    score = 0
    
    if savings_ratio >= 20:
        score += 35
    elif savings_ratio >= 15:
        score += 25
    elif savings_ratio >= 10:
        score += 15
    
    if investment_ratio >= 15:
        score += 35
    elif investment_ratio >= 10:
        score += 25
    elif investment_ratio >= 5:
        score += 15
    
    if discretionary_ratio <= 40:
        score += 30
    elif discretionary_ratio <= 50:
        score += 20
    elif discretionary_ratio <= 60:
        score += 10
    
    if score >= 85:
        return "Excellent"
    elif score >= 70:
        return "Good"
    elif score >= 50:
        return "Fair"
    else:
        return "Needs Improvement"

def display_ai_advisor(analysis):
    """Display AI advisor analysis"""
    print("\n" + "="*80)
    print(" "*28 + "AI FINANCIAL ADVISOR")
    print("="*80)
    
    print(f"\n📊 ALLOCATION HEALTH: {analysis['allocation_health']}")
    
    if analysis['identified_leaks']:
        print(f"\n⚠️  IDENTIFIED ISSUES:")
        for i, leak in enumerate(analysis['identified_leaks'], 1):
            print(f"   {i}. {leak}")
    
    if analysis['recommendations']:
        print(f"\n💡 RECOMMENDATIONS:")
        for i, rec in enumerate(analysis['recommendations'], 1):
            print(f"   {i}. {rec}")
    
    if analysis['priority_actions']:
        print(f"\n🎯 PRIORITY ACTIONS:")
        for i, action in enumerate(analysis['priority_actions'], 1):
            print(f"   {i}. {action}")
    
    print("="*80 + "\n")

# ============================================================================
# ADVANCED FEATURES
# ============================================================================

def expense_forecasting(monthly_expenses_history):
    """Predict irregular expenses 2-3 months ahead based on historical patterns"""
    if not monthly_expenses_history or len(monthly_expenses_history) < 3:
        return None
    
    predictions = []
    avg_expense = sum(monthly_expenses_history) / len(monthly_expenses_history)
    
    # Detect spikes (expenses > 150% of average)
    spikes = [exp for exp in monthly_expenses_history if exp > avg_expense * 1.5]
    
    if spikes:
        avg_spike = sum(spikes) / len(spikes)
        spike_frequency = len(spikes) / len(monthly_expenses_history)
        
        predictions.append({
            'type': 'Irregular Expense Spike',
            'amount': avg_spike,
            'probability': spike_frequency,
            'timeframe': '2-3 months',
            'suggestion': f'Pre-save ₹{avg_spike/3:,.0f}/month for upcoming spike'
        })
    
    # Detect seasonal patterns (last 3 months trend)
    recent_trend = monthly_expenses_history[-3:]
    if len(recent_trend) == 3:
        if recent_trend[0] < recent_trend[1] < recent_trend[2]:
            increase = recent_trend[2] - recent_trend[0]
            predictions.append({
                'type': 'Upward Spending Trend',
                'amount': recent_trend[2] + (increase / 2),
                'probability': 0.7,
                'timeframe': 'Next month',
                'suggestion': f'Budget may need ₹{increase/2:,.0f} increase'
            })
    
    # If no patterns detected, return baseline forecast
    if not predictions:
        predictions.append({
            'type': 'Stable Spending Pattern',
            'amount': avg_expense,
            'probability': 0.8,
            'timeframe': 'Next 2-3 months',
            'suggestion': f'Maintain current budget of ₹{avg_expense:,.0f}/month'
        })
    
    return predictions

def income_volatility_buffer(income_history):
    """Calculate smoothed budget based on 6-month income average"""
    if not income_history or len(income_history) < 2:
        return None
    
    # Use last 6 months or all available data
    recent_income = income_history[-6:] if len(income_history) >= 6 else income_history
    
    avg_income = sum(recent_income) / len(recent_income)
    min_income = min(recent_income)
    max_income = max(recent_income)
    volatility = ((max_income - min_income) / avg_income) * 100
    
    # Conservative estimate (70% of average if high volatility)
    if volatility > 30:
        safe_budget = avg_income * 0.7
        buffer_needed = avg_income - safe_budget
    else:
        safe_budget = avg_income * 0.85
        buffer_needed = avg_income - safe_budget
    
    return {
        'avg_income': avg_income,
        'volatility_pct': volatility,
        'safe_budget': safe_budget,
        'buffer_needed': buffer_needed,
        'recommendation': 'High volatility' if volatility > 30 else 'Moderate volatility'
    }

def tax_loss_harvesting_tracker(investments_data):
    """Flag underperforming investments for tax optimization"""
    if not investments_data:
        return None
    
    opportunities = []
    
    for inv in investments_data:
        current_value = inv.get('current_value', 0)
        purchase_value = inv.get('purchase_value', 0)
        loss_pct = ((current_value - purchase_value) / purchase_value) * 100 if purchase_value > 0 else 0
        
        if loss_pct < -5:  # Flag losses > 5%
            tax_offset = abs(current_value - purchase_value) * 0.3  # Assume 30% tax bracket
            opportunities.append({
                'name': inv.get('name', 'Unknown'),
                'loss_amount': abs(current_value - purchase_value),
                'loss_pct': abs(loss_pct),
                'tax_offset_benefit': tax_offset,
                'suggestion': 'Consider selling to offset gains'
            })
    
    return opportunities if opportunities else None

def opportunity_cost_calculator(skipped_amount, months, annual_return_pct):
    """Calculate future value lost by skipping investment"""
    r = (annual_return_pct / 100) / 12
    n = months
    
    if r == 0:
        future_value = skipped_amount * n
    else:
        # FV = PMT × [((1 + r)^n - 1) / r]
        future_value = skipped_amount * (((1 + r) ** n - 1) / r)
    
    # Also calculate with compounding
    compounded_value = skipped_amount * ((1 + r) ** n)
    
    return {
        'skipped_monthly': skipped_amount,
        'months': months,
        'annual_return': annual_return_pct,
        'lost_future_value': future_value,
        'lost_compounded_value': compounded_value,
        'total_opportunity_cost': max(future_value, compounded_value)
    }

def display_expense_forecast(predictions):
    """Display expense forecasting results"""
    if not predictions:
        print("\n⚠️  Need at least 3 months of expense data for forecasting")
        return
    
    print(f"\n{'='*80}")
    print(" "*25 + "EXPENSE FORECAST (2-3 Months)")
    print(f"{'='*80}")
    
    for pred in predictions:
        print(f"\n📊 {pred['type']}")
        print(f"   Expected Amount: ₹{pred['amount']:,.0f}")
        print(f"   Probability: {pred['probability']*100:.0f}%")
        print(f"   Timeframe: {pred['timeframe']}")
        print(f"   💡 {pred['suggestion']}")
    
    print(f"{'='*80}\n")

def display_income_buffer(buffer_data):
    """Display income volatility buffer analysis"""
    if not buffer_data:
        print("⚠️  Need at least 2 months of income data")
        return
    
    print(f"\n{'='*80}")
    print(" "*25 + "INCOME VOLATILITY BUFFER")
    print(f"{'='*80}")
    
    print(f"\n6-Month Average Income: ₹{buffer_data['avg_income']:,.0f}")
    print(f"Income Volatility: {buffer_data['volatility_pct']:.1f}% ({buffer_data['recommendation']})")
    print(f"\nRecommended Safe Budget: ₹{buffer_data['safe_budget']:,.0f}")
    print(f"Buffer Reserve Needed: ₹{buffer_data['buffer_needed']:,.0f}")
    
    if buffer_data['volatility_pct'] > 30:
        print(f"\n⚠️  High income volatility detected!")
        print(f"   Build reserve fund of ₹{buffer_data['buffer_needed']*3:,.0f} (3-month buffer)")
    else:
        print(f"\n✓ Moderate volatility. Maintain ₹{buffer_data['buffer_needed']*2:,.0f} buffer")
    
    print(f"{'='*80}\n")

def display_tax_harvesting(opportunities):
    """Display tax-loss harvesting opportunities"""
    if not opportunities:
        print("✓ No tax-loss harvesting opportunities (all investments performing well)")
        return
    
    print(f"\n{'='*80}")
    print(" "*25 + "TAX-LOSS HARVESTING TRACKER")
    print(f"{'='*80}")
    
    print(f"\n{'Investment':<20} {'Loss':<15} {'Loss %':<12} {'Tax Benefit':<15}")
    print("-" * 80)
    
    total_tax_benefit = 0
    for opp in opportunities:
        print(f"{opp['name']:<20} ₹{opp['loss_amount']:<14,.0f} {opp['loss_pct']:<11.1f}% ₹{opp['tax_offset_benefit']:<14,.0f}")
        total_tax_benefit += opp['tax_offset_benefit']
    
    print("-" * 80)
    print(f"{'Total Tax Benefit':<20} {'':<15} {'':<12} ₹{total_tax_benefit:<14,.0f}")
    
    print(f"\n💡 Selling these before year-end can offset ₹{total_tax_benefit:,.0f} in taxes")
    print(f"{'='*80}\n")

def display_opportunity_cost(cost_data):
    """Display opportunity cost analysis"""
    print(f"\n{'='*80}")
    print(" "*25 + "OPPORTUNITY COST ANALYSIS")
    print(f"{'='*80}")
    
    print(f"\nSkipping ₹{cost_data['skipped_monthly']:,.0f}/month for {cost_data['months']} months")
    print(f"at {cost_data['annual_return']:.1f}% annual return:")
    
    print(f"\nFuture Value Lost: ₹{cost_data['lost_future_value']:,.0f}")
    print(f"With Compounding: ₹{cost_data['lost_compounded_value']:,.0f}")
    print(f"\n💰 Total Opportunity Cost: ₹{cost_data['total_opportunity_cost']:,.0f}")
    
    print(f"\n⚠️  Every month delayed = ₹{cost_data['total_opportunity_cost']/cost_data['months']:,.0f} less at goal")
    print(f"{'='*80}\n")

# ============================================================================
# BEHAVIORAL & OPTIMIZATION FEATURES
# ============================================================================

def asset_allocation_optimizer(age, risk_tolerance, timeline_years):
    """Suggest optimal stock/bond/cash allocation based on profile using modern portfolio theory"""
    
    # Base allocations by risk profile (research-backed ratios)
    risk_profiles = {
        'conservative': {
            'base_stocks': 30,
            'base_bonds': 55,
            'base_cash': 15
        },
        'moderate': {
            'base_stocks': 60,
            'base_bonds': 30,
            'base_cash': 10
        },
        'aggressive': {
            'base_stocks': 80,
            'base_bonds': 15,
            'base_cash': 5
        }
    }
    
    profile = risk_profiles.get(risk_tolerance.lower(), risk_profiles['moderate'])
    stock_pct = profile['base_stocks']
    bond_pct = profile['base_bonds']
    cash_pct = profile['base_cash']
    
    # Age adjustment (younger = can take more risk)
    if age < 30:
        age_adj = 10
    elif age < 40:
        age_adj = 5
    elif age < 50:
        age_adj = 0
    elif age < 60:
        age_adj = -10
    else:
        age_adj = -20
    
    # Apply age adjustment (shift from stocks to bonds/cash for older investors)
    if risk_tolerance.lower() != 'conservative':
        stock_pct = max(20, min(85, stock_pct + age_adj))
        remaining = 100 - stock_pct
        bond_pct = remaining * 0.75
        cash_pct = remaining * 0.25
    
    # Timeline adjustment (short timeline = more conservative regardless of risk tolerance)
    if timeline_years < 2:
        # Very short timeline - capital preservation critical
        stock_pct = max(10, stock_pct - 30)
        cash_pct = max(30, cash_pct + 20)
        bond_pct = 100 - stock_pct - cash_pct
    elif timeline_years < 5:
        # Short-medium timeline
        stock_pct = max(20, stock_pct - 15)
        cash_pct = max(15, cash_pct + 10)
        bond_pct = 100 - stock_pct - cash_pct
    
    # Ensure conservative stays conservative regardless of age
    if risk_tolerance.lower() == 'conservative':
        stock_pct = min(stock_pct, 40)  # Cap at 40% for conservative
        remaining = 100 - stock_pct
        bond_pct = remaining * 0.7
        cash_pct = remaining * 0.3
    
    # Final adjustments to ensure valid percentages
    total = stock_pct + bond_pct + cash_pct
    if total != 100:
        # Normalize to 100%
        stock_pct = (stock_pct / total) * 100
        bond_pct = (bond_pct / total) * 100
        cash_pct = (cash_pct / total) * 100
    
    return {
        'stocks': round(stock_pct, 1),
        'bonds': round(bond_pct, 1),
        'cash': round(cash_pct, 1),
        'risk_profile': risk_tolerance.capitalize(),
        'rebalance_trigger': 5  # Rebalance when drift > 5%
    }

def dynamic_reallocation_suggestions(allocation, actual_spending, months_tracked):
    """Suggest fund reallocation based on spending patterns with smart redistribution"""
    
    if months_tracked < 2:
        return None
    
    suggestions = []
    total_surplus = 0
    total_deficit = 0
    
    # Priority for redistribution: 1. Savings, 2. Investments, 3. Personal, 4. Misc
    priority_order = ['savings', 'investments', 'personal', 'misc']
    
    # First pass: identify surpluses and deficits
    category_analysis = {}
    
    for category in allocation.keys():
        allocated = allocation.get(category, 0)
        spent = actual_spending.get(category, 0)
        difference = allocated - spent
        
        category_analysis[category] = {
            'allocated': allocated,
            'spent': spent,
            'difference': difference,
            'usage_pct': (spent / allocated * 100) if allocated > 0 else 0
        }
        
        if difference > 0:  # Surplus (underspent)
            total_surplus += difference
        elif difference < 0:  # Deficit (overspent)
            total_deficit += abs(difference)
    
    # Second pass: create smart reallocation plan
    if total_surplus > 0 or total_deficit > 0:
        
        # Handle deficits first (overspending)
        deficit_categories = []
        for category, data in category_analysis.items():
            if data['difference'] < 0:
                deficit_categories.append({
                    'category': category,
                    'overspend': abs(data['difference']),
                    'allocated': data['allocated'],
                    'spent': data['spent']
                })
        
        # Handle surpluses (underspending)
        surplus_categories = []
        for category, data in category_analysis.items():
            if data['difference'] > 0 and data['usage_pct'] < 85:  # Consistently underspending
                surplus_categories.append({
                    'category': category,
                    'surplus': data['difference'],
                    'allocated': data['allocated'],
                    'spent': data['spent'],
                    'usage_pct': data['usage_pct']
                })
        
        # Create redistribution plan
        if surplus_categories and deficit_categories:
            # Case 1: Have both surplus and deficit - redistribute smartly
            remaining_surplus = total_surplus
            
            for deficit in deficit_categories:
                if remaining_surplus <= 0:
                    break
                
                amount_needed = deficit['overspend']
                amount_to_allocate = min(amount_needed, remaining_surplus)
                
                # Find source of reallocation (lowest priority surplus first)
                sources = []
                temp_surplus = remaining_surplus
                
                for surplus in sorted(surplus_categories, key=lambda x: priority_order.index(x['category']), reverse=True):
                    if temp_surplus <= 0:
                        break
                    contribution = min(surplus['surplus'], amount_to_allocate)
                    if contribution > 0:
                        sources.append(f"₹{contribution:,.0f} from {surplus['category']}")
                        temp_surplus -= contribution
                
                suggestions.append({
                    'type': 'deficit_coverage',
                    'category': deficit['category'],
                    'allocated': deficit['allocated'],
                    'spent': deficit['spent'],
                    'action': f"Cover ₹{amount_to_allocate:,.0f} overspend using: {', '.join(sources)}",
                    'priority': 'High'
                })
                
                remaining_surplus -= amount_to_allocate
            
            # If surplus remains after covering deficits, reallocate by priority
            if remaining_surplus > 0:
                for priority_cat in priority_order:
                    if priority_cat in [s['category'] for s in surplus_categories]:
                        continue  # Skip categories that had surplus
                    
                    suggestions.append({
                        'type': 'surplus_reallocation',
                        'category': priority_cat,
                        'allocated': allocation.get(priority_cat, 0),
                        'spent': actual_spending.get(priority_cat, 0),
                        'action': f"Boost by ₹{remaining_surplus:,.0f} from underspent categories",
                        'priority': 'Medium'
                    })
                    break
        
        elif surplus_categories and not deficit_categories:
            # Case 2: Only surplus - allocate to high priority categories
            # Allocate surplus to savings first, then investments
            for priority_cat in ['savings', 'investments']:
                if total_surplus > 0:
                    sources = [f"₹{s['surplus']:,.0f} from {s['category']}" for s in surplus_categories]
                    
                    suggestions.append({
                        'type': 'surplus_reallocation',
                        'category': priority_cat,
                        'allocated': allocation.get(priority_cat, 0),
                        'spent': actual_spending.get(priority_cat, 0),
                        'action': f"Redirect ₹{total_surplus:,.0f} surplus to boost {priority_cat}. Sources: {', '.join(sources)}",
                        'priority': 'High'
                    })
                    break
        
        elif deficit_categories and not surplus_categories:
            # Case 3: Only deficit - need to increase income or reduce spending
            for deficit in deficit_categories:
                suggestions.append({
                    'type': 'deficit_warning',
                    'category': deficit['category'],
                    'allocated': deficit['allocated'],
                    'spent': deficit['spent'],
                    'action': f"Overspent by ₹{deficit['overspend']:,.0f}. Reduce next month or increase allocation.",
                    'priority': 'High'
                })
        
        # Add efficiency suggestions for consistent underspending
        for surplus in surplus_categories:
            if surplus['usage_pct'] < 70:  # Consistently using <70%
                suggestions.append({
                    'type': 'efficiency_tip',
                    'category': surplus['category'],
                    'allocated': surplus['allocated'],
                    'spent': surplus['spent'],
                    'action': f"Using only {surplus['usage_pct']:.0f}% - consider reducing allocation by ₹{surplus['surplus']:,.0f}",
                    'priority': 'Low'
                })
    
    return suggestions if suggestions else None

def micro_savings_triggers(transactions, savings_threshold=50):
    """Convert small budget wins into automatic savings"""
    
    if not transactions:
        return None
    
    triggers = []
    total_micro_savings = 0
    
    for trans in transactions:
        category = trans.get('category', '')
        budgeted = trans.get('budgeted', 0)
        actual = trans.get('actual', 0)
        
        if actual < budgeted:
            saved = budgeted - actual
            if saved >= savings_threshold:
                triggers.append({
                    'category': category,
                    'budgeted': budgeted,
                    'actual': actual,
                    'saved': saved,
                    'action': 'Auto-transfer to investments'
                })
                total_micro_savings += saved
    
    return {
        'triggers': triggers,
        'total_micro_savings': total_micro_savings
    } if triggers else None

def streak_tracking(monthly_performance, goal_type='budget_adherence'):
    """Track financial discipline streaks"""
    
    if not monthly_performance or len(monthly_performance) < 1:
        return None
    
    current_streak = 0
    longest_streak = 0
    temp_streak = 0
    
    for month in monthly_performance:
        success = month.get('success', False)
        
        if success:
            temp_streak += 1
            longest_streak = max(longest_streak, temp_streak)
        else:
            temp_streak = 0
    
    # Current streak is the last consecutive successes
    for month in reversed(monthly_performance):
        if month.get('success', False):
            current_streak += 1
        else:
            break
    
    success_count = sum(1 for m in monthly_performance if m.get('success', False))
    success_rate = (success_count / len(monthly_performance)) * 100
    
    # Determine milestone
    milestone = None
    if current_streak >= 12:
        milestone = "🏆 1 Year Streak! Financial Master!"
    elif current_streak >= 6:
        milestone = "🥇 6 Month Streak! Keep going!"
    elif current_streak >= 3:
        milestone = "🥈 3 Month Streak! Building momentum!"
    elif current_streak >= 1:
        milestone = "🥉 Starting strong!"
    
    return {
        'current_streak': current_streak,
        'longest_streak': longest_streak,
        'success_rate': success_rate,
        'total_months': len(monthly_performance),
        'milestone': milestone,
        'goal_type': goal_type
    }

def display_asset_allocation(allocation_data, monthly_investment=None):
    """Display asset allocation recommendations"""
    print(f"\n{'='*80}")
    print(" "*25 + "ASSET ALLOCATION OPTIMIZER")
    print(f"{'='*80}")
    
    print(f"\nRisk Profile: {allocation_data['risk_profile']}")
    print(f"\nRecommended Allocation:")
    
    if monthly_investment and monthly_investment > 0:
        stock_amount = (allocation_data['stocks'] / 100) * monthly_investment
        bond_amount = (allocation_data['bonds'] / 100) * monthly_investment
        cash_amount = (allocation_data['cash'] / 100) * monthly_investment
        
        print(f"  📈 Stocks:  {allocation_data['stocks']}%  →  ₹{stock_amount:,.0f}/month")
        print(f"  📊 Bonds:   {allocation_data['bonds']}%  →  ₹{bond_amount:,.0f}/month")
        print(f"  💵 Cash:    {allocation_data['cash']}%  →  ₹{cash_amount:,.0f}/month")
        print(f"\n  Total Investment: ₹{monthly_investment:,.0f}/month")
    else:
        print(f"  📈 Stocks:  {allocation_data['stocks']}%")
        print(f"  📊 Bonds:   {allocation_data['bonds']}%")
        print(f"  💵 Cash:    {allocation_data['cash']}%")
    
    print(f"\n💡 Rebalance when any category drifts >{allocation_data['rebalance_trigger']}%")
    
    # Give specific guidance
    if allocation_data['stocks'] >= 70:
        print("⚠️  High stock allocation - suitable for long-term aggressive growth")
    elif allocation_data['stocks'] <= 40:
        print("✓ Conservative allocation - suitable for capital preservation")
    else:
        print("✓ Balanced allocation - good mix of growth and stability")
    
    print(f"{'='*80}\n")

def display_dynamic_reallocation(suggestions):
    """Display dynamic reallocation suggestions"""
    if not suggestions:
        print("\n✓ All categories being used efficiently. No reallocation needed.")
        return
    
    print(f"\n{'='*80}")
    print(" "*25 + "DYNAMIC REALLOCATION SUGGESTIONS")
    print(f"{'='*80}")
    
    # Group by type
    deficit_coverage = [s for s in suggestions if s.get('type') == 'deficit_coverage']
    surplus_realloc = [s for s in suggestions if s.get('type') == 'surplus_reallocation']
    deficit_warnings = [s for s in suggestions if s.get('type') == 'deficit_warning']
    efficiency_tips = [s for s in suggestions if s.get('type') == 'efficiency_tip']
    
    if deficit_coverage:
        print("\n🔴 OVERSPENDING COVERAGE PLAN:")
        print("-" * 80)
        for sug in deficit_coverage:
            print(f"\n{sug['category'].upper()}: Allocated ₹{sug['allocated']:,.0f} | Spent ₹{sug['spent']:,.0f}")
            print(f"   💡 {sug['action']}")
    
    if surplus_realloc:
        print("\n🟢 SURPLUS REALLOCATION:")
        print("-" * 80)
        for sug in surplus_realloc:
            print(f"\n{sug['category'].upper()}: Allocated ₹{sug['allocated']:,.0f} | Spent ₹{sug['spent']:,.0f}")
            print(f"   💡 {sug['action']}")
    
    if deficit_warnings:
        print("\n⚠️  BUDGET OVERRUNS:")
        print("-" * 80)
        for sug in deficit_warnings:
            print(f"\n{sug['category'].upper()}: Allocated ₹{sug['allocated']:,.0f} | Spent ₹{sug['spent']:,.0f}")
            print(f"   💡 {sug['action']}")
    
    if efficiency_tips:
        print("\n💡 EFFICIENCY OPTIMIZATION:")
        print("-" * 80)
        for sug in efficiency_tips:
            print(f"\n{sug['category'].upper()}: Allocated ₹{sug['allocated']:,.0f} | Spent ₹{sug['spent']:,.0f}")
            print(f"   💡 {sug['action']}")
    
    print(f"\n{'='*80}\n")

def display_micro_savings(micro_data):
    """Display micro-savings triggers"""
    if not micro_data:
        print("\n✓ No micro-savings opportunities this period")
        return
    
    print(f"\n{'='*80}")
    print(" "*25 + "MICRO-SAVINGS TRIGGERS")
    print(f"{'='*80}")
    
    print(f"\n{'Category':<15} {'Budgeted':<12} {'Actual':<12} {'Saved':<12} {'Action':<20}")
    print("-" * 80)
    
    for trigger in micro_data['triggers']:
        print(f"{trigger['category'].capitalize():<15} ₹{trigger['budgeted']:<11,.0f} ₹{trigger['actual']:<11,.0f} ₹{trigger['saved']:<11,.0f} {trigger['action']}")
    
    print("-" * 80)
    print(f"{'Total Micro-Savings':<15} {'':<12} {'':<12} ₹{micro_data['total_micro_savings']:<11,.0f}")
    
    print(f"\n💰 Auto-transfer ₹{micro_data['total_micro_savings']:,.0f} to investments")
    print(f"{'='*80}\n")

def display_streak_tracking(streak_data):
    """Display streak tracking results"""
    if not streak_data:
        print("\n⚠️  Need at least 1 month of performance data")
        return
    
    print(f"\n{'='*80}")
    print(" "*25 + "FINANCIAL DISCIPLINE STREAK")
    print(f"{'='*80}")
    
    print(f"\n🔥 Current Streak: {streak_data['current_streak']} months")
    print(f"🏆 Longest Streak: {streak_data['longest_streak']} months")
    print(f"📊 Success Rate: {streak_data['success_rate']:.1f}% ({streak_data['total_months']} months tracked)")
    
    if streak_data['milestone']:
        print(f"\n{streak_data['milestone']}")
    
    # Motivation messages
    if streak_data['current_streak'] == 0:
        print("\n💪 Start fresh this month! Every expert was once a beginner.")
    elif streak_data['current_streak'] < 3:
        print("\n💪 Keep pushing! Consistency builds wealth.")
    
    print(f"{'='*80}\n")

# ============================================================================
# STRATEGIC & INTELLIGENT FEATURES
# ============================================================================

def goal_conflict_resolver(goals, monthly_income, current_allocation):
    """Prioritize and resolve competing financial goals using intelligent scoring"""
    
    if not goals or len(goals) < 2:
        return None
    
    # Score each goal
    scored_goals = []
    
    for goal in goals:
        urgency_score = calculate_urgency_score(goal.get('deadline_months', 12))
        roi_score = calculate_roi_score(goal.get('expected_return', 0), goal.get('timeline_months', 12))
        feasibility_score = calculate_feasibility_score(
            goal.get('monthly_required', 0),
            monthly_income,
            current_allocation
        )
        
        total_score = (urgency_score * 0.4) + (roi_score * 0.3) + (feasibility_score * 0.3)
        
        scored_goals.append({
            'name': goal.get('name', 'Unnamed Goal'),
            'target_amount': goal.get('target_amount', 0),
            'monthly_required': goal.get('monthly_required', 0),
            'deadline_months': goal.get('deadline_months', 12),
            'expected_return': goal.get('expected_return', 0),
            'urgency_score': urgency_score,
            'roi_score': roi_score,
            'feasibility_score': feasibility_score,
            'total_score': total_score,
            'priority': 'High' if total_score >= 7 else 'Medium' if total_score >= 5 else 'Low'
        })
    
    # Sort by total score (highest first)
    scored_goals.sort(key=lambda x: x['total_score'], reverse=True)
    
    return scored_goals

def calculate_urgency_score(deadline_months):
    """Score based on urgency (0-10 scale)"""
    if deadline_months <= 3:
        return 10
    elif deadline_months <= 6:
        return 8
    elif deadline_months <= 12:
        return 6
    elif deadline_months <= 24:
        return 4
    else:
        return 2

def calculate_roi_score(expected_return, timeline_months):
    """Score based on return on investment (0-10 scale)"""
    if timeline_months == 0:
        return 0
    
    annualized_return = (expected_return / timeline_months) * 12
    
    if annualized_return >= 15:
        return 10
    elif annualized_return >= 12:
        return 8
    elif annualized_return >= 8:
        return 6
    elif annualized_return >= 5:
        return 4
    else:
        return 2

def calculate_feasibility_score(monthly_required, monthly_income, current_allocation):
    """Score based on how feasible the goal is (0-10 scale)"""
    available_funds = monthly_income - sum(current_allocation.values())
    
    if monthly_required == 0:
        return 5
    
    coverage_ratio = available_funds / monthly_required if monthly_required > 0 else 0
    
    if coverage_ratio >= 1.5:
        return 10
    elif coverage_ratio >= 1.0:
        return 8
    elif coverage_ratio >= 0.7:
        return 6
    elif coverage_ratio >= 0.5:
        return 4
    else:
        return 2

def market_aware_advisor(current_market_conditions, investment_allocation, risk_tolerance):
    """Provide strategic investment advice based on market conditions"""
    
    if not current_market_conditions:
        return None
    
    market_status = current_market_conditions.get('status', 'neutral').lower()
    volatility = current_market_conditions.get('volatility', 'medium').lower()
    
    recommendations = []
    allocation_adjustments = {}
    
    # Market conditions analysis
    if market_status == 'dip' or market_status == 'correction':
        # Opportunity to buy during dips (dollar-cost averaging advantage)
        if risk_tolerance.lower() in ['moderate', 'aggressive']:
            increase_pct = 15 if risk_tolerance.lower() == 'aggressive' else 10
            increase_amount = investment_allocation * (increase_pct / 100)
            
            recommendations.append({
                'type': 'opportunity',
                'action': f'Consider increasing investment by {increase_pct}% (₹{increase_amount:,.0f})',
                'reasoning': 'Market dip presents buying opportunity for long-term gains',
                'risk_level': 'Medium'
            })
            
            allocation_adjustments['increase_investment'] = increase_amount
        else:
            recommendations.append({
                'type': 'caution',
                'action': 'Maintain current investment allocation',
                'reasoning': 'Conservative profile - stay the course during volatility',
                'risk_level': 'Low'
            })
    
    elif market_status == 'peak' or market_status == 'overvalued':
        # Market at peak - be cautious
        recommendations.append({
            'type': 'caution',
            'action': 'Maintain or slightly reduce equity exposure',
            'reasoning': 'Market appears overvalued - protect gains and build cash reserves',
            'risk_level': 'Low'
        })
        
        if risk_tolerance.lower() != 'aggressive':
            recommendations.append({
                'type': 'rebalancing',
                'action': 'Shift 10% from stocks to bonds/cash',
                'reasoning': 'Lock in profits and increase stability',
                'risk_level': 'Low'
            })
    
    elif market_status == 'neutral' or market_status == 'stable':
        # Normal conditions - stick to plan
        recommendations.append({
            'type': 'steady',
            'action': 'Continue regular investment schedule',
            'reasoning': 'Market conditions normal - maintain disciplined approach',
            'risk_level': 'Low'
        })
    
    # Volatility-based advice
    if volatility == 'high':
        recommendations.append({
            'type': 'volatility_warning',
            'action': 'Increase emergency fund by 1 month expenses',
            'reasoning': 'High volatility period - strengthen financial buffer',
            'risk_level': 'Medium'
        })
    
    return {
        'market_status': market_status.capitalize(),
        'volatility': volatility.capitalize(),
        'recommendations': recommendations,
        'allocation_adjustments': allocation_adjustments
    }

def inflation_adjuster(goals, current_inflation_rate):
    """Auto-adjust goal targets based on inflation to maintain purchasing power"""
    
    if not goals or current_inflation_rate <= 0:
        return None
    
    adjusted_goals = []
    
    for goal in goals:
        original_target = goal.get('target_amount', 0)
        timeline_years = goal.get('timeline_months', 12) / 12
        
        # Calculate inflation-adjusted target: FV = PV * (1 + inflation)^years
        adjusted_target = original_target * ((1 + (current_inflation_rate / 100)) ** timeline_years)
        inflation_impact = adjusted_target - original_target
        
        # Recalculate monthly requirement
        timeline_months = goal.get('timeline_months', 12)
        expected_return = goal.get('expected_return', 0)
        
        if expected_return > 0:
            # With investment returns
            r = (expected_return / 100) / 12
            adjusted_monthly = adjusted_target * r / (((1 + r) ** timeline_months) - 1)
        else:
            # Simple savings
            adjusted_monthly = adjusted_target / timeline_months
        
        original_monthly = goal.get('monthly_required', 0)
        monthly_increase = adjusted_monthly - original_monthly
        
        adjusted_goals.append({
            'name': goal.get('name', 'Unnamed Goal'),
            'original_target': original_target,
            'adjusted_target': adjusted_target,
            'inflation_impact': inflation_impact,
            'original_monthly': original_monthly,
            'adjusted_monthly': adjusted_monthly,
            'monthly_increase': monthly_increase,
            'timeline_years': timeline_years,
            'inflation_rate': current_inflation_rate
        })
    
    return adjusted_goals

def bank_feed_simulator(monthly_income, allocation, variance=0.1):
    """Simulate bank transactions and auto-categorize them (placeholder for real API)"""
    
    # This simulates what a real bank API integration would do
    import random
    
    transactions = []
    categories_map = {
        'savings': ['Transfer to Savings', 'Fixed Deposit', 'Recurring Deposit'],
        'investments': ['Mutual Fund SIP', 'Stock Purchase', 'ETF Investment', 'PPF Deposit'],
        'personal': ['Shopping', 'Dining', 'Entertainment', 'Clothing', 'Electronics'],
        'misc': ['Groceries', 'Transportation', 'Utilities', 'Phone Bill', 'Internet']
    }
    
    for category, allocated_amount in allocation.items():
        # Generate 2-4 transactions per category
        num_transactions = random.randint(2, 4)
        remaining = allocated_amount
        
        for i in range(num_transactions):
            if i == num_transactions - 1:
                amount = remaining
            else:
                # Random amount with variance
                base = allocated_amount / num_transactions
                amount = base * (1 + random.uniform(-variance, variance))
                amount = max(0, min(amount, remaining))
            
            if amount > 0:
                transactions.append({
                    'category': category,
                    'description': random.choice(categories_map.get(category, ['Other'])),
                    'amount': round(amount, 2),
                    'auto_categorized': True,
                    'confidence': random.uniform(0.85, 0.99)
                })
                remaining -= amount
    
    # Calculate category totals
    category_totals = {}
    for trans in transactions:
        cat = trans['category']
        category_totals[cat] = category_totals.get(cat, 0) + trans['amount']
    
    return {
        'transactions': transactions,
        'category_totals': category_totals,
        'total_transactions': len(transactions),
        'auto_categorized_count': len([t for t in transactions if t['auto_categorized']]),
        'avg_confidence': sum(t['confidence'] for t in transactions) / len(transactions) if transactions else 0
    }

def display_goal_conflict_resolver(scored_goals, monthly_income):
    """Display prioritized goals with intelligent scoring"""
    if not scored_goals:
        print("\n⚠️  Need at least 2 goals for conflict resolution")
        return
    
    print(f"\n{'='*80}")
    print(" "*25 + "GOAL CONFLICT RESOLVER")
    print(f"{'='*80}")
    
    print(f"\nTotal Goals: {len(scored_goals)} | Available Income: ₹{monthly_income:,.0f}")
    print("\n" + "-" * 80)
    
    for i, goal in enumerate(scored_goals, 1):
        print(f"\n#{i} [{goal['priority']}] {goal['name'].upper()}")
        print(f"   Target: ₹{goal['target_amount']:,.0f} | Monthly: ₹{goal['monthly_required']:,.0f} | Timeline: {goal['deadline_months']} months")
        print(f"   📊 Scores: Urgency {goal['urgency_score']:.1f} | ROI {goal['roi_score']:.1f} | Feasibility {goal['feasibility_score']:.1f} | Total {goal['total_score']:.1f}")
    
    print("\n" + "=" * 80)
    print("\n💡 RECOMMENDATION:")
    print(f"   Focus on top {min(2, len(scored_goals))} goals first for optimal resource allocation")
    
    total_required = sum(g['monthly_required'] for g in scored_goals[:2])
    if total_required > monthly_income:
        print(f"   ⚠️  Top 2 goals need ₹{total_required:,.0f}/month - consider timeline adjustment")
    else:
        print(f"   ✓ Top 2 goals achievable with ₹{total_required:,.0f}/month ({(total_required/monthly_income)*100:.1f}% of income)")
    
    print(f"{'='*80}\n")

def display_market_aware_advisor(advisor_data):
    """Display market-aware investment recommendations"""
    if not advisor_data:
        print("\n⚠️  Market data required")
        return
    
    print(f"\n{'='*80}")
    print(" "*25 + "MARKET-AWARE ADVISOR")
    print(f"{'='*80}")
    
    print(f"\n📊 Current Market: {advisor_data['market_status']} | Volatility: {advisor_data['volatility']}")
    print("\n" + "-" * 80)
    
    for rec in advisor_data['recommendations']:
        risk_icon = "🔴" if rec['risk_level'] == 'High' else "🟡" if rec['risk_level'] == 'Medium' else "🟢"
        print(f"\n{risk_icon} [{rec['type'].upper()}]")
        print(f"   Action: {rec['action']}")
        print(f"   Reasoning: {rec['reasoning']}")
    
    if advisor_data['allocation_adjustments']:
        print("\n" + "-" * 80)
        print("📈 SUGGESTED ADJUSTMENTS:")
        for key, value in advisor_data['allocation_adjustments'].items():
            print(f"   • {key.replace('_', ' ').title()}: ₹{value:,.0f}")
    
    print(f"\n{'='*80}\n")

def display_inflation_adjuster(adjusted_goals):
    """Display inflation-adjusted goals"""
    if not adjusted_goals:
        print("\n⚠️  No goals to adjust for inflation")
        return
    
    print(f"\n{'='*80}")
    print(" "*25 + "INFLATION ADJUSTER")
    print(f"{'='*80}")
    
    total_impact = sum(g['inflation_impact'] for g in adjusted_goals)
    total_monthly_increase = sum(g['monthly_increase'] for g in adjusted_goals)
    
    print(f"\nInflation Rate: {adjusted_goals[0]['inflation_rate']:.1f}% annually")
    print("\n" + "-" * 80)
    
    for goal in adjusted_goals:
        print(f"\n{goal['name'].upper()} ({goal['timeline_years']:.1f} years)")
        print(f"   Original Target:  ₹{goal['original_target']:>12,.0f}  →  Monthly: ₹{goal['original_monthly']:>10,.0f}")
        print(f"   Adjusted Target:  ₹{goal['adjusted_target']:>12,.0f}  →  Monthly: ₹{goal['adjusted_monthly']:>10,.0f}")
        print(f"   Inflation Impact: ₹{goal['inflation_impact']:>12,.0f}  →  Increase: ₹{goal['monthly_increase']:>10,.0f}/month")
    
    print("\n" + "=" * 80)
    print(f"\n💰 Total Impact: ₹{total_impact:,.0f} | Additional Monthly: ₹{total_monthly_increase:,.0f}")
    print("💡 Targets auto-adjusted to maintain purchasing power")
    print(f"{'='*80}\n")

def display_bank_feed_integration(feed_data):
    """Display simulated bank feed integration results"""
    if not feed_data:
        print("\n⚠️  No transaction data")
        return
    
    print(f"\n{'='*80}")
    print(" "*25 + "BANK FEED INTEGRATION")
    print(f"{'='*80}")
    
    print(f"\nTotal Transactions: {feed_data['total_transactions']}")
    print(f"Auto-Categorized: {feed_data['auto_categorized_count']} ({feed_data['avg_confidence']*100:.1f}% avg confidence)")
    
    print("\n" + "-" * 80)
    print(f"{'Category':<15} {'Transactions':<15} {'Total Amount':<15}")
    print("-" * 80)
    
    for category, total in feed_data['category_totals'].items():
        trans_count = len([t for t in feed_data['transactions'] if t['category'] == category])
        print(f"{category.capitalize():<15} {trans_count:<15} ₹{total:<14,.0f}")
    
    print("\n💡 All transactions automatically categorized using ML")
    print("📊 Ready for budget tracking and analysis")
    print(f"{'='*80}\n")