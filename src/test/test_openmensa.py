from unittest import TestCase
from pyopenmensa.feed import LazyBuilder
from datetime import date
from menu_parser import FMIBistroMenuParser
from entities import Dish, Price, Menu, Week
import openmensa

class OpenMensaTest(TestCase):
    def test_Should_Add_Dish_to_Canteen(self):
        canteen = LazyBuilder()
        dateobj = date(2017, 3, 27)
        dish = Dish("Gulasch vom Schwein", Price(1.9), set(["S", "Gl", "GlG", "GlW", "Kn", "Mi"]), "Tagesgericht")

        openmensa.addDishToCanteen(dish, dateobj, canteen)
        meal = canteen._days[dateobj]['Speiseplan'][0]
        self.assertEqual(meal[0], "Gulasch vom Schwein")
        self.assertEqual(meal[2], {'other': 190})

    def test_Should_Add_Week_to_Canteen(self):
        date_mon2 = date(2017, 11, 6)
        date_tue2 = date(2017, 11, 7)
        date_wed2 = date(2017, 11, 8)
        date_thu2 = date(2017, 11, 9)
        date_fri2 = date(2017, 11, 10)
        dish_aktion2 = Dish("Pochiertes Lachsfilet mit Dillsoße dazu Minze-Reis", Price(6.5), set(["Sl", "Mi"]), "Tagesgericht")
        dish1_mon2 = Dish("Dampfkartoffeln mit Zucchinigemüse", Price(3.6), set(["Sl"]), "Tagesgericht")
        dish2_mon2 = Dish("Valess-Schnitzel mit Tomaten-Couscous", Price(4.3), set(["Sl", "Gl", "Ei", "Mi"]), "Tagesgericht")
        dish3_mon2 = Dish("Kasslerpfanne mit frischen Champignons und Spätzle", Price(4.9), set(["Sl", "Mi"]), "Tagesgericht")
        dish1_tue2 = Dish("Gemüsereispfanne mit geräuchertem Tofu", Price(3.6), set(["Sl"]), "Tagesgericht")
        dish2_tue2 = Dish("Schweineschnitzel in Karottenpanade mit Rosmarin- Risoleekartoffeln", Price(5.3), set(["Sl", "Gl", "Ei"]), "Tagesgericht")
        dish1_wed2 = Dish("Spaghetti al Pomodoro", Price(3.6), set(["Sl", "Gl"]), "Tagesgericht")
        dish2_wed2 = Dish("Krustenbraten vom Schwein mit Kartoffelknödel und Krautsalat", Price(5.3), set(["Sl", "Gl"]), "Tagesgericht")
        dish1_thu2 = Dish("Red-Thaicurrysuppe mit Gemüse und Kokosmilch", Price(2.9), set(["Sl"]), "Tagesgericht")
        dish2_thu2 = Dish("Senf-Eier mit Salzkartoffeln", Price(3.8), set(["Sl", "Sf", "Mi"]), "Tagesgericht")
        dish3_thu2 = Dish("Putengyros mit Zaziki und Tomatenreis", Price(5.3), set(["Sl", "Mi"]), "Tagesgericht")
        dish1_fri2 = Dish("Spiralnudeln mit Ratatouillegemüse", Price(3.6), set(["Gl"]), "Tagesgericht")
        dish2_fri2 = Dish("Milchreis mit warmen Sauerkirschen", Price(3), set(["Mi"]), "Tagesgericht")
        dish3_fri2 = Dish("Lasagne aus Seelachs und Blattspinat", Price(5.3), set(["Sl", "Gl", "Mi"]), "Tagesgericht")
        menu_mon2 = Menu(date_mon2, [dish_aktion2, dish1_mon2, dish2_mon2, dish3_mon2])
        menu_tue2 = Menu(date_tue2, [dish_aktion2, dish1_tue2, dish2_tue2])
        menu_wed2 = Menu(date_wed2, [dish_aktion2, dish1_wed2, dish2_wed2])
        menu_thu2 = Menu(date_thu2, [dish_aktion2, dish1_thu2, dish2_thu2, dish3_thu2])
        menu_fri2 = Menu(date_fri2, [dish_aktion2, dish1_fri2, dish2_fri2, dish3_fri2])
        week = Week(45, 2017, [menu_mon2, menu_tue2, menu_wed2, menu_thu2, menu_fri2])
        week = {}
        week[date_mon2] = menu_mon2
        week[date_tue2] = menu_tue2
        week[date_wed2] = menu_wed2
        week[date_thu2] = menu_thu2
        week[date_fri2] = menu_fri2
        weeks = Week.to_weeks(week)

        canteen = openmensa.weeksToCanteenFeed(weeks)
        self.assertEqual(canteen.hasMealsFor(date_mon2), True)
        self.assertEqual(canteen.hasMealsFor(date_tue2), True)
        self.assertEqual(canteen.hasMealsFor(date_wed2), True)
        self.assertEqual(canteen.hasMealsFor(date_thu2), True)
        self.assertEqual(canteen.hasMealsFor(date_fri2), True)
        
        canteen_wed2 = canteen._days[date_wed2]['Speiseplan']
        self.assertEqual(canteen_wed2[0], ("Pochiertes Lachsfilet mit Dillsoße dazu Minze-Reis", [], {'other': 650}))
        self.assertEqual(canteen_wed2[1], ("Spaghetti al Pomodoro", [], {'other': 360}))
        self.assertEqual(canteen_wed2[2], ("Krustenbraten vom Schwein mit Kartoffelknödel und Krautsalat", [], {'other': 530}))
        
