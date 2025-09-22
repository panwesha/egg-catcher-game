from graphics import Canvas
from datetime import datetime
import random
import time
import math
import sys
    
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400

sun_element = []
moon_element = []

# Sizes of BASKET and EGG 
BASKET_HEIGHT = 20
BASKET_WIDTH = 60
EGG_HEIGHT = 20
EGG_WIDTH = 15

# Details of Gameplay
FALL_START_SPEED = 7
FALL_INCREMENT = 0.01
MAX_LIVES = 3

# Remove all objects in the 'elements' from the canvas and from the lists
def clear_elements(canvas, element):
    for obj_id in element:
        canvas.delete(obj_id)
    element.clear()

# Environment and Background Functions
# Create the background or the sky color on the canvas
def create_sky_color():
    hour = datetime.now().hour
    
    if 6 <= hour < 18:
        return 'skyblue'        #Day
    else:
        return 'midnightblue'   #Night

# Draw the sky with stars, also if it is night time
def draw_sky(canvas):
    sky_color = create_sky_color()
    canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, sky_color)
    # Add stars if night
    if sky_color == "midnightblue":
        for i in range(40):
            x = random.randint(0, CANVAS_WIDTH)
            y = random.randint(0, CANVAS_HEIGHT // 2)
            canvas.create_oval(x, y, x+2, y+2, "white")
    return sky_color

# Draw the Sun with outward rays on top right corner of the canvas
def draw_sun(canvas):
    # Sun settings (top-right corner)
    sun_x = 360
    sun_y = 50
    sun_radius = 15
    ray_length = 20
    num_rays = 20  # Number of rays
    #sun_teil =[]
    # Draw the sun (yellow circle)
    sun = canvas.create_oval(
        sun_x - sun_radius,
        sun_y - sun_radius,
        sun_x + sun_radius,
        sun_y + sun_radius,
        "yellow"
    )
    sun_element.append(sun)
    
# Create outward rays for the sun
    for i in range(num_rays):
        angle = (2 * math.pi / num_rays) * i
        # Start on the edge of the sun
        start_x = sun_x + math.cos(angle) * sun_radius
        start_y = sun_y + math.sin(angle) * sun_radius
        # End farther out
        end_x = sun_x + math.cos(angle) * (sun_radius + ray_length)
        end_y = sun_y + math.sin(angle) * (sun_radius + ray_length)

        ray_id = canvas.create_line(start_x, start_y, end_x, end_y, color = "orange")
        sun_element.append(ray_id)
    return sun_element
# Pause so the window stays open for a while
    time.sleep(0.08)

# Draw the moon on the canvas for night period
def draw_moon(canvas):
    # Simple crescent moon (white circle + dark overlay)
    moon = canvas.create_oval(330, 30, 380, 80, "white", "gray")
    shadow = canvas.create_oval(340, 30, 390, 80, "midnightblue", "midnightblue")
    return [moon, shadow]

# Create cloud
def draw_cloud(canvas, x, y):
    parts = []
    # for three clouds
    parts.append(canvas.create_oval(
        x,
        y,
        x+40,
        y+25,
        "lightgray",
        "",
    ))
    parts.append(canvas.create_oval(
        x+20,
        y-10,
        x+60,
        y+25,
        "lightgray",
        "",
    ))
    parts.append(canvas.create_oval(
        x+40,
        y,
        x+80,
        y+25,
        "lightgray",
        "",
    ))
    return parts

# Define the Weather Condition
# Create the weather particle such as, raindrops, snow
def create_weather_type(canvas, weather_type):
    x = random.randint(0, CANVAS_WIDTH)
    y = 0
    if weather_type == "rain":
        return canvas.create_line(x, y, x, y + 10, "darkgrey")
    elif weather_type == "snow":
        return canvas.create_oval(x, y, x + 3, y + 3, "white")


# Define the Decorative elements such as grass, flowers
# Create Grass on the bottom of the canvas
def draw_grass(canvas):
    for x in range(0, CANVAS_WIDTH, 5):
        y1 = CANVAS_HEIGHT
        y2 = CANVAS_HEIGHT - random.randint(5, 15)
        canvas.create_line(
            x, 
            y1, 
            x + 2, 
            y2, 
            "darkgreen"
            )

# Create flowers at the bottom of the canvas
def draw_flower(canvas, x, y):
    petal_radius = 4
    petal_color = random.choice(["pink", "red", "orange", "yellow","white"])
    offsets = [(-petal_radius, 0), (petal_radius, 0), (0, -petal_radius), (0, petal_radius)]
    for dx, dy in offsets:
        canvas.create_oval(
        x + dx - petal_radius, 
        y + dy - petal_radius,  
        x + dx + petal_radius, 
        y + dy + petal_radius, 
        petal_color, 
        ""
        )

# Create the center of the flower
    canvas.create_oval(
        x - 2, 
        y - 2, 
        x + 2, 
        y + 2, 
        "yellow", 
        ""
        )
# Create the Stem of the flower
    canvas.create_rectangle(
        x - 1,
        y + 2, 
        x + 1, 
        y + 12, 
        "green", 
        ""
        )
# Define the main elements of this game Such as, Basket and Eggs
# Create the basket with rim
def create_basket(canvas, x, y, width=80, height=40, basket_color="saddlebrown", rim_color="brown"):
    """
    Draws a basket at (x, y) with width, height, and colors.
    Returns a list of object ids for later movement or deletion.
    """
    objects = []

    # Basket body
    basket = canvas.create_oval(
        x, y, 
        x + width, y + height, 
        basket_color, 
        "black"
    )
    objects.append(basket)

    # Basket rim (overlay on top part of the basket)
    rim = canvas.create_oval(
        x, y, 
        x + width, y + height / 3, 
        rim_color, 
        "black"
    )
    objects.append(rim)

    return objects

# Create egg
def create_egg(canvas):
        egg_x = random.randint(0, CANVAS_WIDTH - EGG_WIDTH)
        egg_y = 0
        return canvas.create_oval(
            egg_x, 
            egg_y,
            egg_x + EGG_WIDTH, 
            egg_y + EGG_HEIGHT,
            "white", 
            "black"
        )

# Create a bonus item or golden egg
def bonus_item(canvas, bonus_speed=FALL_START_SPEED):
    """
    Create a falling golden egg bonus item at a random top position.
    Returns a dict with the object id and update() method.
    """
    size_w, size_h = 15, 20
    x = random.randint(0, CANVAS_WIDTH - size_w)
    y = 0
    speed = bonus_speed * 1.2

    obj_id = canvas.create_oval(
        x, y,
        x + size_w, y + size_h,
        "gold",
        "brown"
    )

    def update():
        nonlocal y
        y += speed
        canvas.move(obj_id, 0, speed)
        bonus['y'] = y  
        if y > CANVAS_HEIGHT:
            canvas.delete(obj_id)
            return False
        return True

    bonus = {
        'id': obj_id,
        'update': update,
        'x': x,
        'y': y,
        'speed': speed,
    }
    return bonus

# Create the Sparkle effect
def sparkle_effect(canvas, x, y, duration=0.5, sparkle_count=10):
    sparkles = []

    for i in range(sparkle_count):
        # Choose a random angle (0 to 2π)
        angle = random.uniform(0, 2 * math.pi)
        length = random.randint(30, 80)  # Random line length

        dx = math.cos(angle) * length
        dy = math.sin(angle) * length

        # Create line sparkle (in a random color)
        line_color = random.choice(["yellow", "orange", "red", "white"])
        line = canvas.create_line(
            x, y,
            x + dx, y + dy,
            line_color
        )
        sparkles.append(line)

        # Optional small circle at the end
        end_x = x + dx
        end_y = y + dy
        oval = canvas.create_oval(
            end_x - 2, end_y - 2,
            end_x + 2, end_y + 2,
            "white",
            "orange"
        )
        sparkles.append(oval)
    # Animate sparkles fading out and remove them
    start_time = time.time()
    while time.time() - start_time < duration:
        # Just wait for duration (could add fade if supported)
        time.sleep(0.05)
    for sparkle in sparkles:
        canvas.delete(sparkle)

# Create the Play Again State
def play_again_state():
    return {
        'score': 0,
        'lives': MAX_LIVES,
        'fall_speed': FALL_START_SPEED,
        'eggs': [create_egg(canvas)],
        'bonus_items': [],
        'bonus_egg_spawned': False,
        'frame': 0,
    }





#####################################
def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    clear_elements(canvas, sun_element)
    clear_elements(canvas, moon_element)

    sky_color = draw_sky(canvas)

    if sky_color == "skyblue":
        sun_element.extend(draw_sun(canvas))
    else:
        moon_element.extend(draw_moon(canvas))

# Create three clouds at different position with anime effect
    clouds = [
        draw_cloud(canvas, random.randint(0, CANVAS_WIDTH), random.randint(20, 60)),
        draw_cloud(canvas, random.randint(0, CANVAS_WIDTH), random.randint(20, 60)),
        draw_cloud(canvas, random.randint(0, CANVAS_WIDTH), random.randint(20, 60)),
    ]

    cloud_speed = [0.5, 0.3, 0.4]  # different speeds of each cloud

# Draw grass on the canvas
    draw_grass(canvas)

# Draw flowers along the bottom
    for i in range (7):
        x = (CANVAS_WIDTH // 7) * i + 30
        y = CANVAS_HEIGHT - 20
        draw_flower(canvas, x, y)

# Draw the basket
# Basket initial position (top-left corner)
     
    basket_x = CANVAS_WIDTH // 2 - BASKET_WIDTH // 2
    basket_y = CANVAS_HEIGHT - BASKET_HEIGHT - 10
    basket_ids = create_basket(canvas, basket_x, basket_y)


# Draw Eggs
    eggs = [create_egg(canvas)]
    fall_speed = FALL_START_SPEED

    score = 0
    frame = 0
    lives = MAX_LIVES

    Score_Text = canvas.create_text(10, 10, text=f"Score: {score}", font="Arial", font_size=20, color="Yellow")
    Lives_text = canvas.create_text(CANVAS_WIDTH - 100, 10, text=f"Lives: {lives}", font="Arial", font_size=20, color="red")
    weather = random.choice(["clear", "rain", "snow", "sunny"])  # Randomly choose weather
    weather_type = []
    bonus_items = []
    bonus_egg_spawned = False
    
    while True:
        time.sleep(0.02)
        frame +=1
        # Move clouds
        for i, cloud_parts in enumerate(clouds):
            for part in cloud_parts: 
                coords = canvas.coords(part)
                x, y = coords[0], coords[1]
                new_x = x + cloud_speed[i]
                if new_x > CANVAS_WIDTH:
                    new_x = -80  # width of cloud approx
                canvas.moveto(part, new_x, y)
        # Move basket with mouseleft and right 
        # Get current mouse x position
        mouse_x = canvas.get_mouse_x()

        # Center basket on mouse_x, clamp to canvas limits
        basket_x = max(0, min(CANVAS_WIDTH - BASKET_WIDTH, mouse_x - BASKET_WIDTH // 2))

        # Move basket to new position
        canvas.moveto(basket_ids[0], basket_x, basket_y)  # main oval
        canvas.moveto(basket_ids[1], basket_x, basket_y)  # rim
        

# Show the weather type
        if weather in ["rain", "snow"]:
    # Occasionally add a new weather type
            if random.random() < 0.3:
                type = create_weather_type(canvas, weather)
                weather_type.append(type)

    # Switch weather type
            for type in weather_type[:]:
                coords = canvas.coords(type)
                if coords is None:
                    # Particle is already deleted or invalid, remove from list
                    weather_type.remove(type)
                    continue

                x = coords[0]
                y = coords[1]
                canvas.moveto(type, x, y + (6 if weather == "rain" else 2))  # rain falls faster
                if y > CANVAS_HEIGHT:
                
                    canvas.delete(type)
                    weather_type.remove(type)
            #  Show or hide the sun
            for obj_id in sun_element:
                canvas.set_hidden(obj_id, weather in ["rain", "snow"])

                
 # Bonus item           
        if not bonus_egg_spawned and frame > 100:
            bonus_items.append(bonus_item(canvas, bonus_speed = FALL_START_SPEED))
            bonus_egg_spawned = True

        # Update bonus items
        for item in bonus_items[:]:
            still_falling = item['update']()
            if not still_falling:
                bonus_items.remove(item)
            else:
                coords = canvas.coords(item['id'])
                item_x, item_y = coords[0], coords[1]

                if (item_y + EGG_HEIGHT >= basket_y and
                    item_y <= basket_y + BASKET_HEIGHT and
                    item_x + EGG_WIDTH >= basket_x and
                    item_x <= basket_x + BASKET_WIDTH):

                    score += 5  # Bonus points!
                    canvas.change_text(Score_Text, f"Score: {score}")
                    center_x = CANVAS_WIDTH / 2
                    center_y = CANVAS_HEIGHT / 2

                    sparkle_effect(canvas, center_x, center_y, duration=0.2, sparkle_count=20)
            
                    canvas.delete(item['id'])
                    bonus_items.remove(item)

# Fall of the egg  
        for egg in eggs:
            coords = canvas.coords(egg)  # [left_x, top_y, right_x, bottom_y]
            egg_x, egg_y = coords[0], coords[1]
           
            new_egg_y = egg_y + fall_speed

            # Move egg down by fall_speed
            canvas.moveto(egg, egg_x, new_egg_y)
           
            #new_egg_x = egg_x + fall_speed
            # Check for collision with basket
            if (new_egg_y + EGG_HEIGHT >= basket_y and
                new_egg_y <= basket_y + BASKET_HEIGHT and
                egg_x + EGG_WIDTH >= basket_x and
                egg_x <= basket_x + BASKET_WIDTH):

                score += 1
                canvas.change_text(Score_Text, f"Score: {score}") 

                # Run sparkle effect (blocking for a moment)
                center_x = CANVAS_WIDTH / 2
                center_y = CANVAS_HEIGHT / 2
                sparkle_effect(canvas, center_x, center_y, duration=0.2, sparkle_count=20)


                # Reset egg to top at new random x
                new_x = random.randint(0, CANVAS_WIDTH - EGG_WIDTH)
                canvas.moveto(egg, new_x, 0)

                # Increase speed
                fall_speed += FALL_INCREMENT

            # Egg fell past bottom (missed)
            elif new_egg_y > CANVAS_HEIGHT:
                lives -= 1
                canvas.change_text(Lives_text, f"Lives: {lives}")

                if lives == 0:
                    canvas.create_text(
                        CANVAS_WIDTH // 4, CANVAS_HEIGHT // 3,
                        text="GAME OVER 🐣",
                        font="Arial",
                        font_size=30,
                        color="Green"
                    )
                    play_again_text = canvas.create_text(
                        CANVAS_WIDTH // 4, 
                        CANVAS_HEIGHT // 2.2,
                        text="Play Again 🔁",
                        font="Arial", font_size=20, color="cyan"
                    )

                    quit_text = canvas.create_text(
                    CANVAS_WIDTH // 4,
                    CANVAS_HEIGHT // 1.8,
                    text="Quit the Game",
                    font="Arial", font_size=20, color="red"
                    )

                    # Wait for user click to restart
                    while True:
                        click = canvas.get_last_click()
                        if click is not None:
                            x, y = click
                            if (CANVAS_WIDTH // 4 - 100 < x < CANVAS_WIDTH // 4 + 100  and
                                CANVAS_HEIGHT // 2.2 - 15  < y < CANVAS_HEIGHT // 2.2 + 15):
                                
                                # Reset the game state here instead of calling main()
                                canvas.clear()# Clears all previous drawings
                                clear_elements(canvas, sun_element)
                                clear_elements(canvas, moon_element)
                                sky_color = draw_sky(canvas)

                                if sky_color == "skyblue":
                                    sun_element.extend(draw_sun(canvas))
                                else:
                                    moon_element.extend(draw_moon(canvas))
                                                            
                                
                                draw_grass(canvas)
                
                                weather = random.choice(["clear", "rain", "snow", "sunny"])
                                weather_type = []
                                # Redraw flowers
                                for i in range(6):
                                    flower_x = (CANVAS_WIDTH // 6) * i + 30
                                    flower_y = CANVAS_HEIGHT - 20
                                    draw_flower(canvas, flower_x, flower_y)
                                
                                # Redraw clouds
                                clouds = [
                                    draw_cloud(canvas, random.randint(0, CANVAS_WIDTH), random.randint(20, 60)),
                                    draw_cloud(canvas, random.randint(0, CANVAS_WIDTH), random.randint(20, 60)),
                                    draw_cloud(canvas, random.randint(0, CANVAS_WIDTH), random.randint(20, 60)),
                                ]
                                
                                # Reset basket position
                                basket_x = CANVAS_WIDTH // 2 - BASKET_WIDTH // 2
                                basket_y = CANVAS_HEIGHT - BASKET_HEIGHT - 10
                                basket_ids = create_basket(canvas, basket_x, basket_y)
                                
                                # Reset game variables
                                eggs = [create_egg(canvas)]
                                fall_speed = FALL_START_SPEED
                                score = 0
                                lives = MAX_LIVES
                                bonus_items = []
                                bonus_egg_spawned = False
                                frame = 0
                                
                                # Reset UI texts
                                Score_Text = canvas.create_text(10, 10, text=f"Score: {score}", font="Arial", font_size=20, color="Yellow")
                                Lives_text = canvas.create_text(CANVAS_WIDTH - 100, 10, text=f"Lives: {lives}", font="Arial", font_size=20, color="red")
                                
                                break  # Exit restart loop and continue main game loop
                            
                            elif (CANVAS_WIDTH // 4 -50 < x < CANVAS_WIDTH // 4+50  and
                                    CANVAS_HEIGHT // 1.8-10  < y < CANVAS_HEIGHT // 1.8+20 ):
                                canvas.create_text(
                                    CANVAS_WIDTH // 4, 
                                    CANVAS_HEIGHT // 1.6, 
                                    text="Thanks for playing!", 
                                    font="Arial", 
                                    font_size=18, 
                                    color="gray"
                                )
                                time.sleep(2)
                                sys.exit()
                        time.sleep(0.05)
                    continue
                    #return  # End the game
        
                # Reset egg position to top at new random x
                new_x = random.randint(0, CANVAS_WIDTH - EGG_WIDTH)
                canvas.moveto(egg, new_x, 0)
        
if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass  # suppress SystemExit traceback

                        



        
        
    


    
