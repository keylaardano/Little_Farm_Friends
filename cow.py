from animal import Animal

class Cow(Animal):
    def __init__(self, x, y, min_x, max_x, min_y, max_y):
        super().__init__(
            x, y, 
            produce_time_ms=60000, 
            min_x=min_x, max_x=max_x, 
            min_y=min_y, max_y=max_y, 
            gif_path="animal/cow.gif",
            feed_icon_path="menu_bar/cows_feed.png",
            ready_icon_path="animal/Milk.png",
            stop_left_path="animal/cows_stop_left.gif",
            stop_right_path="animal/cows_stop_right.gif"
        )

        self.required_feed = "Cows Feed"
        self.feed_cost = 20

    def produce(self):
        return "Susu"