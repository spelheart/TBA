"""Define the Quest and QuestManager classes"""


class Quest:
    """
    This class represents a quest in the game. A quest has a title, description,
    objectives, completion status, and optional rewards.
    
    Attributes:
        title (str): The title of the quest.
        description (str): The description of the quest.
        objectives (list): List of objectives to complete.
        is_completed (bool): Whether the quest is completed.
        is_active (bool): Whether the quest is currently active.
        reward (str): Optional reward for completing the quest.
    """

    def __init__(self, title, description, objectives=None, reward=None):
        """Initialize a new quest."""
        self.title = title
        self.description = description
        self.objectives = objectives if objectives is not None else []
        self.completed_objectives = []
        self.is_completed = False
        self.is_active = False
        self.reward = reward

    def activate(self):
        """Activate the quest."""
        self.is_active = True
        print(f"\n🗡️  Nouvelle quête activée: {self.title}")
        print(f"📝 {self.description}\n")

    def complete_objective(self, objective, player=None):
        """Mark an objective as completed."""
        if objective in self.objectives and objective not in self.completed_objectives:
            self.completed_objectives.append(objective)
            print(f"✅ Objectif accompli: {objective}")

            # Check if all objectives are completed
            if len(self.completed_objectives) == len(self.objectives):
                self.complete_quest(player)

            return True
        return False

    def complete_quest(self, player=None):
        """Mark the quest as completed and give reward to player."""
        if not self.is_completed:
            self.is_completed = True
            print(f"\n🏆 Quête terminée: {self.title}")
            if self.reward:
                print(f"🎁 Récompense: {self.reward}")
                if player:
                    reward_success = player.add_reward(self.reward)
                    # If reward fails (weight issue), mark quest as not completed
                    if not reward_success:
                        self.is_completed = False
                        # Remove the last completed objective since the quest failed
                        if self.completed_objectives:
                            self.completed_objectives.pop()
                        return
            print()

    def get_status(self):
        """Get the current status of the quest."""
        if not self.is_active:
            return f"❓ {self.title} (Non activée)"
        if self.is_completed:
            return f"✅ {self.title} (Terminée)"
        completed_count = len(self.completed_objectives)
        total_count = len(self.objectives)
        return f"⏳ {self.title} ({completed_count}/{total_count} objectifs)"

    def get_details(self, current_counts=None):
        """Get detailed information about the quest."""
        details = f"\n📋 Quête: {self.title}\n"
        details += f"📖 {self.description}\n"

        if self.objectives:
            details += "\nObjectifs:\n"
            for objective in self.objectives:
                status = "✅" if objective in self.completed_objectives else "⬜"
                objective_text = self._format_objective_with_progress(objective, current_counts)
                details += f"  {status} {objective_text}\n"

        if self.reward:
            details += f"\n🎁 Récompense: {self.reward}\n"

        return details

    def _format_objective_with_progress(self, objective, current_counts):
        """Format an objective with progress information if available."""
        if not current_counts:
            return objective

        for counter_name, current_count in current_counts.items():
            if counter_name not in objective:
                continue

            required = self._extract_number_from_text(objective)
            if required is not None:
                return f"{objective} (Progression: {current_count}/{required})"

        return objective

    def _extract_number_from_text(self, text):
        """Extract the first number from a text string."""
        for word in text.split():
            if word.isdigit():
                return int(word)
        return None

    def check_room_objective(self, room_name, player=None):
        """Check if visiting a specific room completes an objective."""
        room_objectives = [
            f"Visiter {room_name}",
            f"Explorer {room_name}",
            f"Aller à {room_name}",
            f"Entrer dans {room_name}"
        ]

        for objective in room_objectives:
            if self.complete_objective(objective, player):
                return True
        return False

    def check_action_objective(self, action, target=None, player=None):
        """Check if performing an action completes an objective."""
        if target:
            objective_variations = [
                f"{action} {target}",
                f"{action} avec {target}",
                f"{action} le {target}",
                f"{action} la {target}"
            ]
        else:
            objective_variations = [action]

        for objective in objective_variations:
            if self.complete_objective(objective, player):
                return True
        return False

    def check_counter_objective(self, counter_name, current_count, player=None):
        """Check objectives that require counting."""
        for objective in self.objectives:
            if counter_name in objective and objective not in self.completed_objectives:
                words = objective.split()
                for word in words:
                    if word.isdigit():
                        required_count = int(word)
                        if current_count >= required_count:
                            self.complete_objective(objective, player)
                            return True
        return False

    def __str__(self):
        """Return a string representation of the quest."""
        return self.get_status()


class QuestManager:
    """
    This class manages all quests in the game.
    
    Attributes:
        quests (list): List of all quests in the game.
        active_quests (list): List of currently active quests.
        player: Reference to the player object.
    """

    def __init__(self, player=None):
        """Initialize the quest manager."""
        self.quests = []
        self.active_quests = []
        self.player = player

    def add_quest(self, quest):
        """Add a quest to the game."""
        self.quests.append(quest)

    def activate_quest(self, quest_title):
        """Activate a quest by its title."""
        for quest in self.quests:
            if quest.title == quest_title and not quest.is_active:
                quest.activate()
                self.active_quests.append(quest)
                return True
        return False

    def complete_objective(self, objective_text):
        """Complete an objective in any active quest."""
        for quest in self.active_quests:
            if quest.complete_objective(objective_text):
                if quest.is_completed:
                    self.active_quests.remove(quest)
                return True
        return False

    def check_room_objectives(self, room_name):
        """Check all active quests for room-related objectives."""
        for quest in self.active_quests[:]:
            quest.check_room_objective(room_name, self.player)
            if quest.is_completed:
                self.active_quests.remove(quest)

    def check_action_objectives(self, action, target=None):
        """Check all active quests for action-related objectives."""
        for quest in self.active_quests[:]:
            quest.check_action_objective(action, target, self.player)
            if quest.is_completed:
                self.active_quests.remove(quest)

    def check_counter_objectives(self, counter_name, current_count):
        """Check all active quests for counter-related objectives."""
        for quest in self.active_quests[:]:
            quest.check_counter_objective(counter_name, current_count, self.player)
            if quest.is_completed:
                self.active_quests.remove(quest)

    def get_active_quests(self):
        """Get all active quests."""
        return self.active_quests

    def get_all_quests(self):
        """Get all quests."""
        return self.quests

    def get_quest_by_title(self, title):
        """Get a quest by its title."""
        for quest in self.quests:
            if quest.title == title:
                return quest
        return None

    def show_quests(self):
        """Display all quests and their status."""
        if not self.quests:
            print("\nAucune quête disponible.\n")
            return

        print("\n📋 Liste des quêtes:")
        for quest in self.quests:
            print(f"  {quest.get_status()}")
        print()

    def show_quest_details(self, quest_title, current_counts=None):
        """Show detailed information about a specific quest."""
        quest = self.get_quest_by_title(quest_title)
        if quest:
            print(quest.get_details(current_counts))
        else:
            print(f"\nQuête '{quest_title}' non trouvée.\n")
