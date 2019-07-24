def calculate_budget():
    
    from ipywidgets import interact, interactive, widgets
    
    # global total_label
    global budget_label
    global desc_style
    
    global category_labels
    global category_costs
    
    category_labels = {}
    category_costs = {}
    categories = ["HR", "Server", "Operations", "Testing", "Food"]
    
    desc_style = {'description_width': 'initial'}
    
    for category in categories:
        category_labels[category] = widgets.Label(category)
        category_costs[category] = 0
    
    # total_hr_label = widgets.Label("Total HR cost:")
    budget_label = widgets.Label("Total budget:")

    def render_labels():
        # print("Total HR cost: " + str(total_hr_cost))
        # total_hr_label.value = "Total HR cost: " + str(total_hr_cost)
        
        for category in categories:
            category_labels[category].value = category + ": " + str(category_costs[category])

    def on_expense_value_changed(title, category, salary, length):
        # print("Total employee cost: " + str(salary*length))
        calculate_categories_cost()
        calculate_budget()
    
    class Expense(widgets.VBox):
        def __init__(self, *args, **kwargs):
    
            style = {'description_width': 'initial'}
            expense = interactive(on_expense_value_changed,
                                  title = widgets.Text(value= "New Expense", description="Title", style=style),
                                  category = widgets.Dropdown(options=categories,   description="Category", style=style),
                                  salary = widgets.IntSlider(min=1, max=10000, value=1000, description = "Cost per month (€)", style=style),
                                  length = widgets.IntSlider(min=1, max=48, value=1, description="Duration (months)", style=style))
    
            super(Expense, self).__init__()
            self.children = expense.children
    
    def calculate_categories_cost():
        # global total_hr_cost
    
        # total_hr_cost = 0
        for category in categories:
            category_costs[category] = 0
    
        for expense in expenses:
            cost = expense.children[2].value
            duration = expense.children[3].value
            category = expense.children[1].value
    
            category_costs[category] += cost * duration
        # total_hr_cost += cost * duration
    
        render_labels()
    
    def calculate_budget():
        budget = 0
    
        for category in categories:
            budget += category_costs[category]
    
        budget_label.value = "Total budget: " + str(budget)
    
    @interact(expenses_amount=widgets.IntSlider(min=1, max=10, value=1, description="Monthly expenses   amount", style=desc_style))
    def render_expenses(expenses_amount):
        global expenses
        global accordion
    
        # style = {'description_width': 'initial'}
        # employee = interactive(test2, salary=widgets.IntSlider(min=1, max=10000, value=1000,  description="Salary per month (€)", style=style), length=widgets.IntSlider(min=1, max=48,   value=1, description="Job length (months)", style=style))
        # print(employee)
        # item = [widgets.IntSlider(min=1, max=10000, value=1000, description="Salary per month (€)",   style=style), widgets.Label("Job length (months)"), widgets.IntSlider(min=1, max=48,    value=1)]
        # box = widgets.VBox(item)
        expenses = [Expense() for i in range(expenses_amount)]
        # print(expenses[0])
        accordion = widgets.Accordion(expenses)
    
        for index in range(len(expenses)):
            accordion.set_title(index, expenses[index].children[0].value)
    
        display(accordion)
    
        # calculate_total_hr_cost()
        calculate_categories_cost()
        render_labels()
        calculate_budget()
    
    for category in categories:
        category_labels[category].value = category + ": " + str(category_costs[category])
        display(category_labels[category])
    
    # display(total_hr_label)
    print("---------------")
    display(budget_label)
