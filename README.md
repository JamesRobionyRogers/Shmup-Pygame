# shmup 

(Code is inside the folder named "shmup")
I currently have an error when I shoot a meteor (or when i get hit by a meteor), I believe it happens when the explosion animation is trying to happen. Please help if you can, and Thank you very much in advance!      (Note: I am using Python 3.7 is that's any help)

# Errors 
This is the Error when I shoot a meteor: 

Traceback (most recent call last):
  File "C:\Users\James\Desktop\Programing\Programing With Python\KidsCanCode Pygame\game_dev\shmup\004_shmup_v10.py", line 263, in <module>
    expl = Explosion(hit.rect.center, 'lg')
  File "C:\Users\James\Desktop\Programing\Programing With Python\KidsCanCode Pygame\game_dev\shmup\004_shmup_v10.py", line 170, in __init__
    self.image = explosion_anim[self.size][0]
TypeError: 'NoneType' object is not subscriptable
  


And this the Error when I get hit by the meteor:

Traceback (most recent call last):
  File "C:\Users\James\Desktop\Programing\Programing With Python\KidsCanCode Pygame\game_dev\shmup\004_shmup_v10.py", line 272, in <module>
    expl = Explosion(hit.rect.center, 'sm')
  File "C:\Users\James\Desktop\Programing\Programing With Python\KidsCanCode Pygame\game_dev\shmup\004_shmup_v10.py", line 170, in __init__
    self.image = explosion_anim[self.size][0]
TypeError: 'NoneType' object is not subscriptable
  
  
  
  Thank you very much in advance for any help! 
  - Thanks, James 
