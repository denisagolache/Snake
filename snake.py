class Snake:
    def __init__(self, position):
        self.body = [position]
        self.direction = (1, 0)  

    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body = [new_head] + self.body[:-1]

    def grow(self):
        self.body.append(self.body[-1])

    def check_collision(self, obstacles):
        head = self.body[0]
        return (
            head in self.body[1:] or 
            head in obstacles
        )
