from selenium import webdriver
import time


class OdooSession(object):
    """
    Sets up the Chrome browser for automation. Throughout the objects life,
    self.driver is used to access the browser and perform actions on it.
    """

    def __init__(self, url="http://localhost:8069/web"):
        """
        :param url

        Does some setup, does not actually open the browser.
        """
        self.driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.url = url
        self.CurrentApp = ""

    def ChooseDatabase(self, database):
        """
        :param database

        Selects the database to do the work against.
        """
        self.driver.get(self.url)
        self.driver.find_element_by_link_text(database).click()

    def Login(self, username, password):
        """
        :param username
        :param password

        Logs in using the provided credentials. Puts the browser at the app screen.
        """
        login = self.driver.find_element_by_id("login")
        login.clear()
        login.send_keys(username)
        passwd = self.driver.find_element_by_id("password")
        passwd.clear()
        passwd.send_keys(password)
        self.driver.find_element_by_class_name("btn-primary").click()

    def ChooseApp(self, appName):
        """
        :param appName:

        Chooses the selected appName by first going back to the main odoo screen.
        Sets the CurrentApp to appName. After getting to the application screen,
        populates navbar with available navigation selections.
        """
        self.CurrentApp = appName
        self.driver.get(self.url)
        self.driver.find_element_by_link_text(appName).click()
        time.sleep(1)
        self.navbar = self._NavbarButtons()

    def NavbarClick(self, button):
        """
        :param button:

        Clicks the navigation bar button. If there is a submenu, populates menu,
        else clicks to the button to go to whatever screen.
        """
        try:
            i = self.navbar.index(button) + 1
        except ValueError:
            print("%s is not a valid choice for this App. Choices are %r" % (button, self.navbar))
            return
        self.driver.find_element_by_css_selector(
            "#o_navbar_collapse > ul.nav.navbar-nav.o_menu_sections > li:nth-child(%d) > a" % i
        ).click()
        time.sleep(1)
        self.menu = self._MenuButtons()

    def MenuClick(self, button):
        """
        :param button:

        Clicks the submenu button under a navigation button.
        """
        try:
            i = self.menu.index(button) + 1
        except ValueError:
            print("%s is not a valid choice for this Menu. Choices are %r" % (button, self.menu))
            return
        self.driver.find_element_by_css_selector(
            "#o_navbar_collapse > ul.nav.navbar-nav.o_menu_sections > li.open > ul > li:nth-child(%d) > a" % i
        ).click()

    def Snap(self, name="screenshot"):
        """
        :param name:

        Takes a screenshot of the browser and saves it as a png file.
        """
        self.driver.save_screenshot(name + ".png")

    def _NavbarButtons(self):
        """
        Gets a list of items in the navigation bar and returns them as a list.
        """
        nav = self.driver.find_elements_by_css_selector("#o_navbar_collapse > ul.nav.navbar-nav.o_menu_sections")
        return nav[0].text.split("\n")

    def _MenuButtons(self):
        """
        Gets a list of items in the submenu for a navigation button and returns them as a list.
        """
        nav = self.driver.find_elements_by_css_selector(
            "#o_navbar_collapse > ul.nav.navbar-nav.o_menu_sections > li.open > ul"
        )
        return nav[0].text.split("\n")

    def CreateProduct(self, product, *args, **kwargs):
        if self.CurrentApp != "Inventory":
            self.ChooseApp("Inventory")
        self.NavbarClick("Inventory Control")
        self.MenuClick("Products")
        time.sleep(1)

        # clicks the CREATE button
        self.driver.find_element_by_css_selector(
            "body > div.o_control_panel > div.o_cp_left > div.o_cp_buttons > div > button"
        ).click()
        time.sleep(1)
        # fills in product name
        inputs = self.driver.find_elements_by_tag_name("input")
        for input in inputs:
            if input.get_attribute("placeholder") == "Product Name":
                input.send_keys(product)
        # clicks save
        self.driver.find_element_by_css_selector(
            "body > div.o_control_panel.o_breadcrumb_full > div.o_cp_left > div.o_cp_buttons > div > div.o_form_buttons_edit > button.btn.btn-primary.btn-sm.o_form_button_save"
        ).click()

        if "initial" in kwargs:  # does the initial inventory
            time.sleep(1)
            keepers = filter(
                lambda button: button.text == "UPDATE QTY ON HAND", self.driver.find_elements_by_tag_name("button")
            )
            keepers[0].click()
            # So this brings up a modal dialog - figuring out how to deal with this
            dialog = self.driver.find_element_by_css_selector(
                "body > div.modal.in > div > div > div.modal-body.o_act_window > div > div > table"
            )
            rows = filter(
                lambda child: child.tag_name == "tr" and child.text == "New Quantity on Hand",
                dialog.find_elements_by_css_selector("*"),
            )
            rows[0].find_element_by_css_selector("td:nth-child(2) > input").clear()
            rows[0].find_element_by_css_selector("td:nth-child(2) > input").send_keys(kwargs["initial"])
            self.driver.find_element_by_css_selector(
                "body > div.modal.in > div > div > div.modal-footer > div > footer > button.btn.btn-sm.btn-primary"
            ).click()
            time.sleep(1)
            self.driver.find_element_by_css_selector(
                "body > div.o_control_panel > div.o_cp_left > div.o_cp_buttons > div > div.o_form_buttons_view > button.btn.btn-default.btn-sm.o_form_button_create"
            ).click()

    def AdjustInventory(self, sku, amount=1000000):
        """
        :param sku:
        :param amount:

        Only works once per SKU. Designed to be used right after product is created, as there is currently no error
        checking if the option to set initial inventory does not exist.
        """
        if self.CurrentApp != "Inventory":
            self.ChooseApp("Inventory")
        self.NavbarClick("Inventory Control")
        self.MenuClick("Products")
        time.sleep(1)

        self.driver.find_element_by_css_selector(
            "body > div.o_control_panel > div.o_cp_right > div.hidden-xs.btn-group.btn-group-sm.o_cp_switch_buttons > button.btn.btn-icon.fa.fa-lg.fa-list-ul.o_cp_switch_list"
        ).click()
        skustr = format("SKU%07d") % sku
        time.sleep(1)

        # Gets to the product page
        cells = self.driver.find_elements_by_tag_name("td")
        for cell in cells:
            if cell.text == skustr:
                keeper = cell
        keeper.click()

        # gets to the inventory on hand
        self.driver.find_element_by_link_text("INVENTORY").click()

    def CreateCustomer(self, customer):
        pass

    def CreateSale(self, customer, sku):
        """
        :param customer:
        :param sku:

        Macro for creating a Sales Order for the provided customer with 1 item
        identified by the sku. Note that there must be an SKU in the form
        [SKU0000000] where zeros can be any digit.
        """
        if self.CurrentApp != "Sales":
            self.ChooseApp("Sales")
        self.NavbarClick("Sales")
        self.MenuClick("Sales Orders")
        time.sleep(1)

        # clicks the CREATE button
        self.driver.find_element_by_css_selector(
            "body > div.o_control_panel > div.o_cp_left > div.o_cp_buttons > div > button.btn.btn-primary.btn-sm.o_list_button_add"
        ).click()
        time.sleep(1)

        # causes the customer dropdown to appear and then chooses the customer
        dropdowns = self.driver.find_elements_by_css_selector(".o_form_input.ui-autocomplete-input")
        dropdowns[0].click()
        self.driver.find_element_by_link_text(customer).click()

        # Adding an item, clicks the Add an item link, causes product dropdown to show, the selects the SKU
        self.driver.find_element_by_link_text("Add an item").click()
        dropdowns = self.driver.find_elements_by_css_selector(".o_form_input_dropdown")
        dropdowns[8].click()
        skustr = format("[SKU%07d]") % sku
        self.driver.find_element_by_partial_link_text(skustr).click()

        # Saves the sales order
        self.driver.find_element_by_css_selector(
            "body > div.o_content > div > div > div.o_form_statusbar > div.o_statusbar_buttons > button:nth-child(10) > span"
        ).click()
