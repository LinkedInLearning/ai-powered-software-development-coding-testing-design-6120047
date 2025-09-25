class TodoItem:
    def __init__(self, title: str):
        self.title = title
        self.completed = False

    def mark_complete(self):
        self.completed = True

    def mark_incomplete(self):
        self.completed = False

    def __repr__(self):
        status = "✓" if self.completed else "✗"
        return f"[{status}] {self.title}"

task = TodoItem("Buy milk")
print(task)          # [✗] Buy milk
task.mark_complete()
print(task)          # [✓] Buy milk