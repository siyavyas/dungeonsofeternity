class ImageGenerationAgent:
    def generate_asset(self, asset_type):
        if asset_type == "win_screen":
            return "images/youwin.png"
        elif asset_type == "lose_screen":
            return "images/gameover.png"



