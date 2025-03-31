from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai import LLM
import os
import sys
import yaml
from pathlib import Path

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Dungeonsofeternity():
    """Dungeons of Eternity game development crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended

    def __init__(self):
        # Initialize the base class first
        super().__init__()
        
        # Get the project root directory
        self.project_root = Path(__file__).parent.parent.parent
        
        # Set the config paths
        self.agents_config_path = self.project_root / 'src' / 'dungeonsofeternity' / 'config' / 'agents.yaml'
        self.tasks_config_path = self.project_root / 'src' / 'dungeonsofeternity' / 'config' / 'tasks.yaml'
        
        # Load configurations
        try:
            with open(self.agents_config_path, 'r') as f:
                self.agents_config = yaml.safe_load(f)
            with open(self.tasks_config_path, 'r') as f:
                self.tasks_config = yaml.safe_load(f)
        except Exception as e:
            raise Exception(f"Failed to load configuration files: {e}")
        
        # Improved LLM configuration for code generation
        self.llm = LLM(
            model="gpt-4",  # Using GPT-4 for reliable code generation
            temperature=0.1,  # Very low temperature for consistent code generation
            max_tokens=4096,  # Increased context window
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def _create_agent(self, config: dict) -> Agent:
        """Helper method to create agents with consistent configuration"""
        if not isinstance(config, dict):
            raise ValueError(f"Invalid agent configuration: {config}")
            
        required_fields = ['role', 'goal', 'backstory']
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Missing required field '{field}' in agent configuration")
                
        return Agent(
            role=config['role'],
            goal=config['goal'],
            backstory=config['backstory'],
            verbose=True,  # Always verbose for better debugging
            allow_delegation=False,  # Disabled to reduce context size
            llm=self.llm,
            max_iterations=3,  # Reduced from 5 to prevent context overflow
            max_rpm=30,  # Keep rate limit reasonable
        )

    @agent
    def game_designer(self) -> Agent:
        """Create the game designer agent"""
        return self._create_agent(self.agents_config['game_designer'])

    @agent
    def gameplay_programmer(self) -> Agent:
        """Create the gameplay programmer agent"""
        return self._create_agent(self.agents_config['gameplay_programmer'])

    @agent
    def game_engineer(self) -> Agent:
        """Create the game engineer agent"""
        return self._create_agent(self.agents_config['game_engineer'])

    @agent
    def ui_ux_designer(self) -> Agent:
        """Create the UI/UX designer agent"""
        return self._create_agent(self.agents_config['ui_ux_designer'])

    @agent
    def puzzle_designer(self) -> Agent:
        """Create the puzzle designer agent"""
        return self._create_agent(self.agents_config['puzzle_designer'])

    @agent
    def ai_specialist(self) -> Agent:
        """Create the AI specialist agent"""
        return self._create_agent(self.agents_config['ai_specialist'])

    @agent
    def art_director(self) -> Agent:
        """Create the art director agent"""
        return self._create_agent(self.agents_config['art_director'])

    @agent
    def sound_designer(self) -> Agent:
        """Create the sound designer agent"""
        return self._create_agent(self.agents_config['sound_designer'])

    @agent
    def qa_engineer(self) -> Agent:
        """Create the QA engineer agent"""
        return self._create_agent(self.agents_config['qa_engineer'])

    @agent
    def technical_writer(self) -> Agent:
        """Create the technical writer agent"""
        return self._create_agent(self.agents_config['technical_writer'])

    @agent
    def asset_creator(self) -> Agent:
        """Create the asset creator agent"""
        return self._create_agent(self.agents_config['asset_creator'])

    @agent
    def gameplay_balancer(self) -> Agent:
        """Create the gameplay balancer agent"""
        return self._create_agent(self.agents_config['gameplay_balancer'])

    @agent
    def integration_specialist(self) -> Agent:
        """Create the integration specialist agent"""
        return self._create_agent(self.agents_config['integration_specialist'])

    @agent
    def ui_specialist(self) -> Agent:
        """Create the UI specialist agent"""
        return self._create_agent(self.agents_config['ui_specialist'])

    @agent
    def asset_manager(self) -> Agent:
        """Create the asset manager agent"""
        return self._create_agent(self.agents_config['asset_manager'])

    @agent
    def visual_asset_generator(self) -> Agent:
        """Create the visual asset generator agent"""
        return self._create_agent(self.agents_config['visual_asset_generator'])

    @agent
    def character_artist(self) -> Agent:
        """Create the character artist agent"""
        return self._create_agent(self.agents_config['character_artist'])

    @agent
    def card_designer(self) -> Agent:
        """Create the card designer agent"""
        return self._create_agent(self.agents_config['card_designer'])

    @agent
    def background_artist(self) -> Agent:
        """Create the background artist agent"""
        return self._create_agent(self.agents_config['background_artist'])

    def _create_task(self, task_name: str) -> Task:
        """Helper method to create tasks with consistent configuration"""
        if task_name not in self.tasks_config:
            raise ValueError(f"Task '{task_name}' not found in configuration")
            
        task_config = self.tasks_config[task_name]
        if not isinstance(task_config, dict):
            raise ValueError(f"Invalid task configuration for '{task_name}': {task_config}")
            
        # Get the agent name from the task config
        agent_name = task_config.get('agent')
        if not agent_name:
            raise ValueError(f"No agent specified for task '{task_name}'")
            
        # If agent_name is already an Agent object, use it directly
        if isinstance(agent_name, Agent):
            agent = agent_name
        else:
            # Otherwise, try to get the agent by name
            try:
                agent = self._get_agent(agent_name)
            except (AttributeError, ValueError) as e:
                raise ValueError(f"Failed to get agent for task '{task_name}': {str(e)}")
            
        # Create the task with the agent
        return Task(
            description=task_config['description'],
            expected_output=task_config['expected_output'],
            output_file=task_config.get('output_file', f'src/game/{task_name}.py'),
            agent=agent
        )

    def _get_agent(self, agent_name: str) -> Agent:
        """Helper method to get agent by name"""
        if not isinstance(agent_name, str):
            raise TypeError(f"Agent name must be a string, got {type(agent_name)}")
            
        if agent_name not in self.agents_config:
            raise ValueError(f"Agent '{agent_name}' not found in configuration")
            
        try:
            agent_method = getattr(self, agent_name)
            if not callable(agent_method):
                raise ValueError(f"Agent method '{agent_name}' is not callable")
            return agent_method()
        except AttributeError:
            raise ValueError(f"Agent method '{agent_name}' not found")

    @task
    def core_mechanics_design(self) -> Task:
        """Create the core mechanics design task"""
        return self._create_task('core_mechanics_design')

    @task
    def gameplay_implementation(self) -> Task:
        """Create the gameplay implementation task"""
        return self._create_task('gameplay_implementation')

    @task
    def ui_ux_design(self) -> Task:
        """Create the UI/UX design task"""
        return self._create_task('ui_ux_design')

    @task
    def puzzle_design(self) -> Task:
        """Create the puzzle design task"""
        return self._create_task('puzzle_design')

    @task
    def ai_system_design(self) -> Task:
        """Create the AI system design task"""
        return self._create_task('ai_system_design')

    @task
    def art_direction(self) -> Task:
        """Create the art direction task"""
        return self._create_task('art_direction')

    @task
    def sound_design(self) -> Task:
        """Create the sound design task"""
        return self._create_task('sound_design')

    @task
    def quality_assurance(self) -> Task:
        """Create the quality assurance task"""
        return self._create_task('quality_assurance')

    @task
    def technical_documentation(self) -> Task:
        """Create the technical documentation task"""
        return self._create_task('technical_documentation')

    @task
    def core_mechanics_implementation(self) -> Task:
        """Create the core mechanics implementation task"""
        return self._create_task('core_mechanics_implementation')

    @task
    def game_engine_implementation(self) -> Task:
        """Create the game engine implementation task"""
        return self._create_task('game_engine_implementation')

    @task
    def ui_implementation(self) -> Task:
        """Create the UI implementation task"""
        return self._create_task('ui_implementation')

    @task
    def ai_implementation(self) -> Task:
        """Create the AI implementation task"""
        return self._create_task('ai_implementation')

    @task
    def asset_implementation(self) -> Task:
        """Create the asset implementation task"""
        return self._create_task('asset_implementation')

    @task
    def system_integration(self) -> Task:
        """Create the system integration task"""
        return self._create_task('system_integration')

    @task
    def game_launcher(self) -> Task:
        """Create the game launcher task"""
        return self._create_task('game_launcher')

    @task
    def final_integration(self) -> Task:
        """Create the final integration task"""
        return self._create_task('final_integration')

    @task
    def visual_asset_generation(self) -> Task:
        """Create the visual asset generation task"""
        return self._create_task('visual_asset_generation')

    @task
    def character_asset_generation(self) -> Task:
        """Create the character asset generation task"""
        return self._create_task('character_asset_generation')

    @task
    def card_visual_generation(self) -> Task:
        """Create the card visual generation task"""
        return self._create_task('card_visual_generation')

    @task
    def background_asset_generation(self) -> Task:
        """Create the background asset generation task"""
        return self._create_task('background_asset_generation')

    @task
    def asset_integration(self) -> Task:
        """Create the asset integration task"""
        return self._create_task('asset_integration')

    @task
    def ui_improvements(self) -> Task:
        """Create the UI improvements task"""
        return self._create_task('ui_improvements')

    @task
    def asset_loading_fix(self) -> Task:
        """Create the asset loading fix task"""
        return self._create_task('asset_loading_fix')

    @crew
    def crew(self) -> Crew:
        """Create the crew with all tasks in optimal order"""
        # Create all agents first
        agents = {
            'game_designer': self.game_designer(),
            'gameplay_programmer': self.gameplay_programmer(),
            'game_engineer': self.game_engineer(),
            'ui_ux_designer': self.ui_ux_designer(),
            'puzzle_designer': self.puzzle_designer(),
            'ai_specialist': self.ai_specialist(),
            'art_director': self.art_director(),
            'sound_designer': self.sound_designer(),
            'qa_engineer': self.qa_engineer(),
            'technical_writer': self.technical_writer(),
            'asset_creator': self.asset_creator(),
            'gameplay_balancer': self.gameplay_balancer(),
            'integration_specialist': self.integration_specialist(),
            'ui_specialist': self.ui_specialist(),
            'asset_manager': self.asset_manager(),
            'visual_asset_generator': self.visual_asset_generator(),
            'character_artist': self.character_artist(),
            'card_designer': self.card_designer(),
            'background_artist': self.background_artist()
        }
        
        # Create tasks in dependency order with proper context
        tasks = [
            # Phase 1: Core Design (Independent tasks)
            self.core_mechanics_design(),
            self.ui_ux_design(),
            self.puzzle_design(),
            self.ai_system_design(),
            self.art_direction(),
            self.sound_design(),
            
            # Phase 2: Core Implementation (Depends on design)
            self.core_mechanics_implementation(),
            self.game_engine_implementation(),
            self.gameplay_implementation(),
            
            # Phase 3: Feature Implementation (Depends on core)
            self.ui_implementation(),
            self.ai_implementation(),
            self.asset_implementation(),
            
            # Phase 4: Integration (Depends on features)
            self.system_integration(),
            self.game_launcher(),
            self.final_integration(),
            
            # Phase 5: Polish and QA (Depends on integration)
            self.quality_assurance(),
            self.technical_documentation(),
            self.visual_asset_generation(),
            self.character_asset_generation(),
            self.card_visual_generation(),
            self.background_asset_generation(),
            self.asset_integration(),
            self.ui_improvements(),
            self.asset_loading_fix()
        ]

        return Crew(
            agents=list(agents.values()),
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
