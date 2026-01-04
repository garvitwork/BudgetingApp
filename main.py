from functions import *

def main():
    print("\n" + "="*80)
    print(" "*25 + "PERSONAL FINANCE MANAGER")
    print("="*80 + "\n")
    
    # Step 1: Get monthly income
    total_amount = get_float_input("Enter your monthly income (₹): ")
    
    # Step 2: Get allocation percentages
    print("\nEnter allocation percentages (must sum to 100%):")
    
    while True:
        savings_pct = get_float_input("Savings (%): ")
        investment_pct = get_float_input("Investments (%): ")
        personal_pct = get_float_input("Personal Use (%): ")
        
        misc_choice = input("Miscellaneous expenses (default 15%, press Enter or type custom %): ").strip()
        misc_pct = 15 if misc_choice == "" else float(misc_choice)
        
        total_pct = savings_pct + investment_pct + personal_pct + misc_pct
        
        if abs(total_pct - 100) < 0.01:
            break
        else:
            print(f"\n✗ Total = {total_pct}%. Must equal 100%. Try again.\n")
    
    # Step 3: Calculate allocation
    allocation = allocate_budget(total_amount, savings_pct, investment_pct, personal_pct, misc_pct)
    
    # Step 4: Calculate projections
    periods = {
        '1 Month': 1,
        '3 Months': 3,
        '6 Months': 6,
        '12 Months': 12,
        '24 Months': 24
    }
    projections = calculate_projections(allocation, periods)
    
    # Step 5: Display allocation table
    display_allocation_table(projections)
    
    # Step 6: Combined Goals Input
    print("\n" + "="*80)
    print("FINANCIAL GOALS SETUP")
    print("="*80)
    
    # Savings Goal
    print("\n📊 SAVINGS GOAL:")
    savings_target = get_float_input("Enter savings target amount (₹): ")
    savings_months = get_int_input("Enter timeframe (months): ")
    required_monthly_savings = savings_goal_calculator(savings_target, savings_months)
    
    # Investment Goal
    print("\n📈 INVESTMENT GOAL:")
    investment_target = get_float_input("Enter investment target amount (₹): ")
    investment_months = get_int_input("Enter timeframe (months): ")
    annual_return = get_float_input("Enter expected annual return (%): ")
    required_monthly_investment = investment_goal_calculator(
        investment_target, investment_months, annual_return
    )
    
    # Step 7: Combined Goal Analysis & Reallocation Plan
    savings_gap, investment_gap = display_combined_goal_analysis(
        required_monthly_savings,
        required_monthly_investment,
        allocation,
        total_amount
    )
    
    # Step 8: AI Financial Advisor Analysis
    savings_gap = allocation['savings'] - required_monthly_savings
    investment_gap = allocation['investments'] - required_monthly_investment
    
    analysis = generate_ai_analysis(total_amount, allocation, savings_gap, investment_gap)
    display_ai_advisor(analysis)
    
    # Step 9: Summary
    print("="*80)
    print("MONTHLY BUDGET SUMMARY")
    print("="*80)
    for category, amount in allocation.items():
        print(f"{category.capitalize():<15}: ₹{amount:>10,.2f}")
    print("="*80)
    
    # ========================================================================
    # ADVANCED FEATURES
    # ========================================================================
    
    print("\n" + "="*80)
    print(" "*25 + "ADVANCED ANALYTICS")
    print("="*80)
    
    use_advanced = input("\nWould you like to use advanced features? (y/n): ").strip().lower()
    
    if use_advanced == 'y':
        
        # Feature 1: Expense Forecasting
        print("\n" + "="*80)
        print("1. EXPENSE FORECASTING")
        print("="*80)
        
        use_forecast = input("Enter past monthly expenses for forecasting? (y/n): ").strip().lower()
        if use_forecast == 'y':
            num_months = get_int_input("How many months of data? (minimum 3): ", min_val=3)
            expense_history = []
            for i in range(num_months):
                expense = get_float_input(f"Month {i+1} total expenses (₹): ")
                expense_history.append(expense)
            
            predictions = expense_forecasting(expense_history)
            display_expense_forecast(predictions)
        
        # Feature 2: Income Volatility Buffer
        print("="*80)
        print("2. INCOME VOLATILITY BUFFER")
        print("="*80)
        
        use_buffer = input("Enter past monthly income for volatility analysis? (y/n): ").strip().lower()
        if use_buffer == 'y':
            num_months = get_int_input("How many months of income data? (minimum 2): ", min_val=2)
            income_history = []
            for i in range(num_months):
                income = get_float_input(f"Month {i+1} income (₹): ")
                income_history.append(income)
            
            buffer_data = income_volatility_buffer(income_history)
            display_income_buffer(buffer_data)
        
        # Feature 3: Tax-Loss Harvesting Tracker
        print("="*80)
        print("3. TAX-LOSS HARVESTING TRACKER")
        print("="*80)
        
        use_tax = input("Track investments for tax-loss harvesting? (y/n): ").strip().lower()
        if use_tax == 'y':
            num_investments = get_int_input("Number of investments to track: ", min_val=1)
            investments = []
            
            for i in range(num_investments):
                print(f"\nInvestment {i+1}:")
                name = input("  Name: ").strip()
                purchase = get_float_input("  Purchase value (₹): ")
                current = get_float_input("  Current value (₹): ")
                
                investments.append({
                    'name': name,
                    'purchase_value': purchase,
                    'current_value': current
                })
            
            opportunities = tax_loss_harvesting_tracker(investments)
            display_tax_harvesting(opportunities)
        
        # Feature 4: Opportunity Cost Calculator
        print("="*80)
        print("4. OPPORTUNITY COST CALCULATOR")
        print("="*80)
        
        use_opp_cost = input("Calculate opportunity cost of delayed investment? (y/n): ").strip().lower()
        if use_opp_cost == 'y':
            skipped = get_float_input("Monthly investment amount being skipped (₹): ")
            duration = get_int_input("For how many months: ")
            returns = get_float_input("Expected annual return (%): ")
            
            cost_data = opportunity_cost_calculator(skipped, duration, returns)
            display_opportunity_cost(cost_data)
    
    # ========================================================================
    # BEHAVIORAL & OPTIMIZATION FEATURES
    # ========================================================================
    
    print("\n" + "="*80)
    print(" "*20 + "BEHAVIORAL & OPTIMIZATION TOOLS")
    print("="*80)
    
    use_behavioral = input("\nWould you like to use behavioral optimization features? (y/n): ").strip().lower()
    
    if use_behavioral == 'y':
        
        # Feature 5: Asset Allocation Optimizer
        print("\n" + "="*80)
        print("5. ASSET ALLOCATION OPTIMIZER")
        print("="*80)
        
        use_asset = input("Get investment allocation recommendations? (y/n): ").strip().lower()
        if use_asset == 'y':
            age = get_int_input("Enter your age: ", min_val=18)
            print("Risk tolerance: Conservative / Moderate / Aggressive")
            risk = input("Enter risk tolerance: ").strip().lower()
            
            while risk not in ['conservative', 'moderate', 'aggressive']:
                print("Invalid choice. Choose: conservative, moderate, or aggressive")
                risk = input("Enter risk tolerance: ").strip().lower()
            
            timeline = get_int_input("Investment timeline (years): ", min_val=1)
            
            asset_alloc = asset_allocation_optimizer(age, risk, timeline)
            # Pass current monthly investment allocation
            display_asset_allocation(asset_alloc, allocation['investments'])
        
        # Feature 6: Dynamic Reallocation
        print("="*80)
        print("6. DYNAMIC REALLOCATION")
        print("="*80)
        
        use_dynamic = input("Analyze spending patterns for reallocation? (y/n): ").strip().lower()
        if use_dynamic == 'y':
            months = get_int_input("How many months of spending data? (minimum 2): ", min_val=2)
            
            # Get average actual spending
            actual_spending = {}
            for category in ['savings', 'investments', 'personal', 'misc']:
                print(f"\n{category.capitalize()} - Allocated: ₹{allocation[category]:,.0f}")
                spent = get_float_input(f"Average actual spent (₹): ")
                actual_spending[category] = spent
            
            suggestions = dynamic_reallocation_suggestions(allocation, actual_spending, months)
            display_dynamic_reallocation(suggestions)
        
        # Feature 7: Micro-Savings Triggers
        print("="*80)
        print("7. MICRO-SAVINGS TRIGGERS")
        print("="*80)
        
        use_micro = input("Track micro-savings from budget wins? (y/n): ").strip().lower()
        if use_micro == 'y':
            num_trans = get_int_input("Number of categories to track: ", min_val=1)
            transactions = []
            
            for i in range(num_trans):
                print(f"\nCategory {i+1}:")
                cat = input("  Name (e.g., dining, shopping): ").strip()
                budgeted = get_float_input("  Budgeted amount (₹): ")
                actual = get_float_input("  Actual spent (₹): ")
                
                transactions.append({
                    'category': cat,
                    'budgeted': budgeted,
                    'actual': actual
                })
            
            threshold = get_float_input("\nMinimum savings to trigger (₹, default 50): ", min_val=0)
            if threshold == 0:
                threshold = 50
            
            micro_data = micro_savings_triggers(transactions, threshold)
            display_micro_savings(micro_data)
        
        # Feature 8: Streak Tracking
        print("="*80)
        print("8. STREAK TRACKING")
        print("="*80)
        
        use_streak = input("Track financial discipline streak? (y/n): ").strip().lower()
        if use_streak == 'y':
            num_months = get_int_input("How many months to track: ", min_val=1)
            performance = []
            
            print("\nFor each month, did you stay within budget? (y/n)")
            for i in range(num_months):
                month_success = input(f"Month {i+1}: ").strip().lower() == 'y'
                performance.append({'success': month_success})
            
            streak_data = streak_tracking(performance, 'budget_adherence')
            display_streak_tracking(streak_data)
    
    # ========================================================================
    # STRATEGIC INTELLIGENCE FEATURES
    # ========================================================================
    
    print("\n" + "="*80)
    print(" "*20 + "STRATEGIC INTELLIGENCE & OPTIMIZATION")
    print("="*80)
    
    use_strategic = input("\nWould you like to use strategic intelligence features? (y/n): ").strip().lower()
    
    if use_strategic == 'y':
        
        # Feature 9: Goal Conflict Resolver
        print("\n" + "="*80)
        print("9. GOAL CONFLICT RESOLVER")
        print("="*80)
        
        use_goal_resolver = input("Prioritize competing financial goals? (y/n): ").strip().lower()
        if use_goal_resolver == 'y':
            num_goals = get_int_input("Number of goals to evaluate (minimum 2): ", min_val=2)
            goals = []
            
            for i in range(num_goals):
                print(f"\nGoal {i+1}:")
                name = input("  Name: ").strip()
                target = get_float_input("  Target amount (₹): ")
                timeline = get_int_input("  Timeline (months): ")
                expected_return = get_float_input("  Expected annual return (%, 0 for savings): ", min_val=0)
                
                # Calculate monthly required
                if expected_return > 0:
                    r = (expected_return / 100) / 12
                    monthly_req = target * r / (((1 + r) ** timeline) - 1) if timeline > 0 else 0
                else:
                    monthly_req = target / timeline if timeline > 0 else 0
                
                goals.append({
                    'name': name,
                    'target_amount': target,
                    'timeline_months': timeline,
                    'deadline_months': timeline,
                    'expected_return': expected_return,
                    'monthly_required': monthly_req
                })
            
            scored_goals = goal_conflict_resolver(goals, total_amount, allocation)
            display_goal_conflict_resolver(scored_goals, total_amount)
        
        # Feature 10: Market-Aware Advisor
        print("="*80)
        print("10. MARKET-AWARE ADVISOR")
        print("="*80)
        
        use_market = input("Get market-aware investment advice? (y/n): ").strip().lower()
        if use_market == 'y':
            print("\nMarket Status: dip / neutral / peak")
            market_status = input("Current market status: ").strip().lower()
            
            while market_status not in ['dip', 'neutral', 'peak', 'correction', 'overvalued', 'stable']:
                print("Choose: dip, correction, neutral, stable, peak, overvalued")
                market_status = input("Current market status: ").strip().lower()
            
            print("\nVolatility: low / medium / high")
            volatility = input("Current volatility: ").strip().lower()
            
            while volatility not in ['low', 'medium', 'high']:
                print("Choose: low, medium, high")
                volatility = input("Current volatility: ").strip().lower()
            
            print("\nYour Risk Tolerance: conservative / moderate / aggressive")
            risk_tol = input("Risk tolerance: ").strip().lower()
            
            while risk_tol not in ['conservative', 'moderate', 'aggressive']:
                print("Choose: conservative, moderate, aggressive")
                risk_tol = input("Risk tolerance: ").strip().lower()
            
            market_conditions = {
                'status': market_status,
                'volatility': volatility
            }
            
            advisor_data = market_aware_advisor(market_conditions, allocation['investments'], risk_tol)
            display_market_aware_advisor(advisor_data)
        
        # Feature 11: Inflation Adjuster
        print("="*80)
        print("11. INFLATION ADJUSTER")
        print("="*80)
        
        use_inflation = input("Adjust goals for inflation? (y/n): ").strip().lower()
        if use_inflation == 'y':
            inflation_rate = get_float_input("Current inflation rate (% annually): ", min_val=0)
            num_goals = get_int_input("Number of goals to adjust: ", min_val=1)
            
            goals_to_adjust = []
            for i in range(num_goals):
                print(f"\nGoal {i+1}:")
                name = input("  Name: ").strip()
                target = get_float_input("  Target amount (₹): ")
                timeline = get_int_input("  Timeline (months): ")
                expected_return = get_float_input("  Expected annual return (%, 0 for savings): ", min_val=0)
                
                # Calculate monthly required
                if expected_return > 0:
                    r = (expected_return / 100) / 12
                    monthly_req = target * r / (((1 + r) ** timeline) - 1) if timeline > 0 else 0
                else:
                    monthly_req = target / timeline if timeline > 0 else 0
                
                goals_to_adjust.append({
                    'name': name,
                    'target_amount': target,
                    'timeline_months': timeline,
                    'expected_return': expected_return,
                    'monthly_required': monthly_req
                })
            
            adjusted_goals = inflation_adjuster(goals_to_adjust, inflation_rate)
            display_inflation_adjuster(adjusted_goals)
        
        # Feature 12: Bank Feed Integration (Simulated)
        print("="*80)
        print("12. BANK FEED INTEGRATION (DEMO)")
        print("="*80)
        
        use_bank_feed = input("Simulate bank transaction categorization? (y/n): ").strip().lower()
        if use_bank_feed == 'y':
            print("\n🔄 Simulating bank API integration...")
            print("   (In production, this would connect to Plaid/bank APIs)")
            
            feed_data = bank_feed_simulator(total_amount, allocation)
            display_bank_feed_integration(feed_data)
    
    print("\n" + "="*80)
    print("✅ COMPLETE FINANCIAL INTELLIGENCE SYSTEM READY")
    print("="*80)
    print("\n💡 All 12 features activated for optimal wealth creation")
    print("📊 Safe, strategic, and intelligent financial planning")
    print("🎯 Review insights and execute your optimized financial plan")
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    main()