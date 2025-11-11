"""
Management command to create sample financial literacy articles
"""
from django.core.management.base import BaseCommand
from finance_app.models import Article


class Command(BaseCommand):
    help = 'Creates sample financial literacy articles'

    def handle(self, *args, **options):
        sample_articles = [
            {
                'title': 'The 50/30/20 Budget Rule: A Simple Guide to Managing Your Money',
                'summary': 'Learn how to allocate your income effectively using the popular 50/30/20 budgeting rule. This method helps you balance needs, wants, and savings.',
                'content': '''The 50/30/20 budget rule is one of the most popular and straightforward budgeting methods. It divides your after-tax income into three categories:

**50% for Needs:**
- Housing (rent/mortgage)
- Utilities (electricity, water, internet)
- Groceries
- Transportation (car payment, gas, public transit)
- Insurance (health, auto, home)
- Minimum debt payments

**30% for Wants:**
- Dining out
- Entertainment (movies, subscriptions)
- Shopping (non-essential items)
- Hobbies
- Travel

**20% for Savings and Debt Repayment:**
- Emergency fund
- Retirement savings (401k, IRA)
- Investments
- Extra debt payments beyond minimums
- Other savings goals

**How to Get Started:**
1. Calculate your monthly after-tax income
2. Multiply by 0.50, 0.30, and 0.20 to get your budget amounts
3. Track your spending in each category
4. Adjust as needed based on your personal situation

Remember, this is a guideline. If you live in a high-cost area, your needs might be 60% instead of 50%. The key is finding a balance that works for you while prioritizing savings.''',
                'category': 'Budgeting',
                'author': 'Finance Team',
                'is_featured': True
            },
            {
                'title': 'Building an Emergency Fund: Your Financial Safety Net',
                'summary': 'Discover why an emergency fund is crucial and learn practical steps to build one. Start small and grow your financial security over time.',
                'content': '''An emergency fund is money set aside to cover unexpected expenses or financial emergencies. It's your financial safety net that prevents you from going into debt when life throws curveballs.

**Why You Need an Emergency Fund:**
- Medical emergencies
- Job loss
- Car repairs
- Home repairs
- Unexpected travel
- Major appliance replacement

**How Much Should You Save?**
- **Starter Goal:** $1,000 (covers small emergencies)
- **Short-term Goal:** 3 months of expenses
- **Long-term Goal:** 6-12 months of expenses

**Where to Keep Your Emergency Fund:**
- High-yield savings account (easily accessible, earns interest)
- Money market account
- Separate account from your checking (reduces temptation)

**How to Build It:**
1. Start small - aim for $500-$1,000 first
2. Set up automatic transfers
3. Save windfalls (tax refunds, bonuses)
4. Cut one expense and redirect to savings
5. Use the "pay yourself first" principle

**Tips for Success:**
- Make it automatic - set up recurring transfers
- Start with whatever you can afford, even $25/month
- Don't touch it unless it's a true emergency
- Replenish it after using it
- Celebrate milestones to stay motivated

Building an emergency fund takes time, but every dollar saved brings you closer to financial security.''',
                'category': 'Savings',
                'author': 'Finance Team',
                'is_featured': True
            },
            {
                'title': 'Understanding Compound Interest: Make Your Money Work for You',
                'summary': 'Learn how compound interest can help your savings grow exponentially over time. Start investing early to maximize the power of compounding.',
                'content': '''Compound interest is often called the "eighth wonder of the world" because it allows your money to grow exponentially over time. Understanding this concept is crucial for building long-term wealth.

**What is Compound Interest?**
Compound interest is interest calculated on the initial principal plus all accumulated interest from previous periods. In simple terms, you earn interest on your interest.

**Example:**
If you invest $1,000 at 7% annual interest:
- Year 1: $1,000 × 1.07 = $1,070
- Year 2: $1,070 × 1.07 = $1,144.90
- Year 10: $1,967.15
- Year 30: $7,612.26

**The Power of Starting Early:**
Starting to invest at age 25 vs. 35 can make a huge difference:
- Investing $200/month from age 25-65 at 7% = $525,000
- Starting at 35 with the same parameters = $245,000

**Where to Benefit from Compound Interest:**
- Retirement accounts (401k, IRA)
- High-yield savings accounts
- Investment accounts (stocks, bonds, mutual funds)
- Certificates of Deposit (CDs)

**Key Takeaways:**
1. Start as early as possible
2. Invest consistently
3. Reinvest dividends and interest
4. Be patient - time is your greatest asset
5. Don't withdraw early - let it compound

Remember: The best time to start investing was yesterday. The second best time is today.''',
                'category': 'Investing',
                'author': 'Finance Team',
                'is_featured': True
            },
            {
                'title': 'Smart Ways to Reduce Monthly Expenses',
                'summary': 'Practical tips to cut your monthly spending without sacrificing your lifestyle. Small changes can add up to significant savings.',
                'content': '''Reducing monthly expenses is one of the fastest ways to improve your financial situation. Here are practical strategies that can save you hundreds or even thousands of dollars per year:

**Review and Negotiate Bills:**
- Call service providers (internet, cable, phone) to negotiate better rates
- Compare insurance rates annually and switch if you find better deals
- Bundle services for discounts
- Ask about loyalty discounts or retention offers

**Cut Subscription Costs:**
- Audit all subscriptions (streaming, apps, memberships)
- Cancel unused subscriptions
- Share family plans when possible
- Rotate streaming services instead of having all at once

**Reduce Food Expenses:**
- Meal plan and prep to reduce eating out
- Buy generic brands
- Use coupons and cashback apps
- Shop with a list to avoid impulse buys
- Buy in bulk for non-perishables
- Cook at home more often

**Lower Utility Bills:**
- Use programmable thermostats
- Switch to LED bulbs
- Unplug electronics when not in use
- Wash clothes in cold water
- Take shorter showers
- Seal windows and doors for better insulation

**Transportation Savings:**
- Carpool or use public transit
- Walk or bike for short trips
- Maintain your car to improve fuel efficiency
- Compare gas prices using apps
- Consider if you really need that second car

**Shopping Smart:**
- Wait 24-48 hours before making non-essential purchases
- Buy used items when possible
- Use cashback credit cards (pay off monthly!)
- Shop during sales and clearance events
- Avoid shopping when emotional or stressed

**Track Your Spending:**
The first step to reducing expenses is knowing where your money goes. Track every expense for a month to identify areas for improvement.

**Set Savings Goals:**
When you reduce an expense, immediately transfer that amount to savings. This reinforces the habit and grows your savings faster.''',
                'category': 'Budgeting',
                'author': 'Finance Team',
                'is_featured': False
            },
            {
                'title': 'Credit Cards: Friend or Foe?',
                'summary': 'Learn how to use credit cards wisely to build credit and earn rewards, while avoiding the pitfalls of debt and high interest.',
                'content': '''Credit cards can be powerful financial tools when used responsibly, but they can also lead to debt and financial stress if misused. Understanding how to use them wisely is essential.

**Benefits of Credit Cards:**
- Build credit history and improve credit score
- Earn rewards (cashback, points, miles)
- Purchase protection and fraud protection
- Convenience and security
- Emergency backup option
- Track spending easily

**Dangers of Credit Cards:**
- High interest rates (often 15-25% APR)
- Easy to overspend
- Minimum payments keep you in debt
- Fees (annual, late payment, over-limit)
- Can damage credit if misused

**Best Practices:**
1. **Pay in Full Each Month:** Avoid interest charges entirely
2. **Pay On Time:** Late payments hurt your credit and cost money
3. **Keep Utilization Low:** Use less than 30% of your credit limit
4. **Don't Cash Advance:** Extremely high fees and interest
5. **Read the Fine Print:** Understand fees, rates, and terms
6. **Monitor Statements:** Check for errors or fraudulent charges

**When to Use Credit Cards:**
- Planned purchases you can pay off immediately
- Online shopping (better fraud protection)
- Building credit history
- Earning rewards on regular expenses
- Travel (hotel holds, car rentals)

**When to Avoid Credit Cards:**
- You can't pay the balance in full
- Emergency expenses (use emergency fund instead)
- Impulse purchases
- Cash advances
- When you're already in debt

**If You're in Credit Card Debt:**
1. Stop using the cards
2. Pay more than minimum payments
3. Consider balance transfer cards (0% APR offers)
4. Use debt avalanche or snowball method
5. Seek help if needed (credit counseling)

Remember: Credit cards are tools, not free money. Treat them like debit cards - only spend what you have.''',
                'category': 'Credit',
                'author': 'Finance Team',
                'is_featured': False
            },
            {
                'title': 'Retirement Planning: Start Early, Retire Comfortably',
                'summary': 'Essential guide to retirement planning. Learn about different retirement accounts and strategies to secure your financial future.',
                'content': '''Retirement planning is one of the most important aspects of personal finance. Starting early gives you the advantage of time and compound interest.

**Why Start Early?**
- More time for investments to grow
- Smaller monthly contributions needed
- Compound interest works in your favor
- Less financial stress later in life

**Types of Retirement Accounts:**

**401(k) Plans:**
- Employer-sponsored retirement plan
- Pre-tax contributions reduce taxable income
- Many employers offer matching contributions (free money!)
- Contribution limit: $23,000/year (2024)
- Withdrawals taxed as income in retirement

**IRAs (Individual Retirement Accounts):**
- Traditional IRA: Pre-tax contributions, taxed in retirement
- Roth IRA: After-tax contributions, tax-free withdrawals
- Contribution limit: $7,000/year (2024)
- More investment options than 401(k)

**How Much Should You Save?**
- General rule: 15% of your income
- At least contribute enough to get employer match
- Aim to save 10-12x your annual salary by retirement age
- Use retirement calculators to determine your specific needs

**Retirement Planning Steps:**
1. **Start Now:** Even small amounts matter
2. **Take Employer Match:** Don't leave free money on the table
3. **Increase Contributions:** Raise by 1% each year
4. **Diversify Investments:** Don't put all eggs in one basket
5. **Review Annually:** Adjust as your situation changes
6. **Avoid Early Withdrawals:** Penalties and taxes hurt

**Common Mistakes:**
- Waiting too long to start
- Not taking employer match
- Being too conservative or too aggressive
- Cashing out when changing jobs
- Not increasing contributions over time

**Action Items:**
- Enroll in your employer's 401(k) if available
- Open an IRA if no employer plan
- Set up automatic contributions
- Review and adjust your portfolio annually
- Educate yourself on investment basics

Remember: The best retirement plan is the one you start today, not tomorrow.''',
                'category': 'Investing',
                'author': 'Finance Team',
                'is_featured': False
            },
            {
                'title': 'Debt Payoff Strategies: Get Out of Debt Faster',
                'summary': 'Compare the debt snowball and avalanche methods to find the best strategy for paying off your debts efficiently.',
                'content': '''Getting out of debt requires a plan and discipline. Here are two proven strategies to help you become debt-free faster:

**Debt Snowball Method:**
Pay off debts from smallest to largest balance, regardless of interest rate.

**How it works:**
1. List all debts from smallest to largest
2. Pay minimums on all debts
3. Put extra money toward smallest debt
4. Once paid off, roll that payment to next smallest
5. Repeat until all debts are paid

**Pros:**
- Quick wins boost motivation
- Fewer bills to manage faster
- Psychological momentum

**Cons:**
- May pay more interest overall
- Ignores interest rates

**Debt Avalanche Method:**
Pay off debts from highest to lowest interest rate, regardless of balance.

**How it works:**
1. List all debts by interest rate (highest first)
2. Pay minimums on all debts
3. Put extra money toward highest interest debt
4. Once paid off, roll that payment to next highest
5. Repeat until all debts are paid

**Pros:**
- Saves the most money on interest
- Mathematically optimal
- Faster overall payoff

**Cons:**
- May take longer to see first payoff
- Requires more discipline

**Which Method to Choose?**
- Choose Snowball if you need motivation and quick wins
- Choose Avalanche if you want to save the most money
- Either method works - the key is consistency

**Additional Tips:**
- Stop accumulating new debt
- Create a budget to find extra money
- Consider balance transfer cards (0% APR offers)
- Negotiate lower interest rates
- Consider debt consolidation if it makes sense
- Get a side job for extra income
- Sell unused items to make extra payments

**Stay Motivated:**
- Track your progress visually
- Celebrate milestones
- Join a support group or find an accountability partner
- Remember your "why" - why you want to be debt-free

The best debt payoff strategy is the one you'll stick with. Choose a method and commit to it!''',
                'category': 'Debt',
                'author': 'Finance Team',
                'is_featured': False
            },
            {
                'title': 'Understanding Your Credit Score',
                'summary': 'Learn what affects your credit score and how to improve it. A good credit score opens doors to better interest rates and financial opportunities.',
                'content': '''Your credit score is a three-digit number that represents your creditworthiness. It affects your ability to get loans, credit cards, and even rent apartments. Understanding how it works is crucial.

**What is a Credit Score?**
A credit score typically ranges from 300 to 850. Higher scores indicate better creditworthiness:
- 800-850: Excellent
- 740-799: Very Good
- 670-739: Good
- 580-669: Fair
- 300-579: Poor

**Factors That Affect Your Score:**

**1. Payment History (35%):**
- Most important factor
- On-time payments boost your score
- Late payments hurt significantly
- Set up autopay to avoid mistakes

**2. Credit Utilization (30%):**
- Amount of credit you're using vs. available
- Keep below 30% (ideally under 10%)
- High utilization suggests financial stress
- Pay down balances to improve

**3. Length of Credit History (15%):**
- How long you've had credit accounts
- Older accounts are better
- Don't close old accounts unnecessarily
- Start building credit early

**4. Credit Mix (10%):**
- Variety of credit types (cards, loans, mortgage)
- Shows you can handle different credit types
- Not a major factor, but helps

**5. New Credit (10%):**
- Recent credit inquiries and new accounts
- Too many hard inquiries hurt
- Space out credit applications
- Rate shopping within 14-45 days counts as one inquiry

**How to Improve Your Credit Score:**
1. Pay all bills on time (set reminders or autopay)
2. Keep credit card balances low
3. Don't close old credit cards
4. Limit new credit applications
5. Check your credit report for errors
6. Become an authorized user (if responsible)
7. Pay off debt, don't just move it around
8. Be patient - improvements take time

**Check Your Credit Report:**
- Free annual reports from AnnualCreditReport.com
- Check for errors and dispute them
- Monitor for identity theft
- Review all three bureaus (Equifax, Experian, TransUnion)

**Common Myths:**
- Checking your own credit hurts your score (false - soft inquiries don't hurt)
- Closing cards improves your score (false - can hurt utilization)
- You need to carry a balance (false - pay in full is best)
- Income affects your score (false - not a factor)

Remember: Building good credit takes time and consistent responsible behavior. Start today!''',
                'category': 'Credit',
                'author': 'Finance Team',
                'is_featured': False
            }
        ]

        created_count = 0
        for article_data in sample_articles:
            article, created = Article.objects.get_or_create(
                title=article_data['title'],
                defaults={
                    'summary': article_data.get('summary', ''),
                    'content': article_data.get('content', ''),
                    'category': article_data.get('category', ''),
                    'author': article_data.get('author', ''),
                    'is_featured': article_data.get('is_featured', False)
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created article: {article.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Article already exists: {article.title}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully created {created_count} new articles!')
        )





