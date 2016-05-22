import mcpi.minecraft as minecraft # Load libraries
import mcpi.block as block
import time, datetime, psutil

time.sleep(1)
mc=minecraft.Minecraft.create() # Connect to Minecraft
keepblocks=[block.AIR.id,block.WATER.id,block.LAVA.id,block.SNOW.id,block.WATER_FLOWING.id,block.WATER_STATIONARY]
counter = 0 # A bunch of variables to keep track of how many blocks have been processed
num_blocks = 1000 # How many blocks to transform before pausing to let Minecraft catch-up
start = time.time()
for x in range(-128,128): # the x-direction
    for y in range(-4,35): # the y-direction (up/down)
        for z in range(-128,128): # the z-direction
            print(x,y,z)
            test = mc.getBlock(x,y,z) # Read a block at x,y,z
            if test not in keepblocks: # Don't transform these blocks (should always contain AIR)
                counter+=1
                if counter > num_blocks:
                    counter = 0
                    time.sleep(5) # Pause to allow Minecraft catch-up
                mc.setBlock(x,y,z,block.REDSTONE_ORE.id) # <- set this: the block to which you want other transformed
                print('Changing Block: ' + str(test) + ' (counter = ' + str(counter) + ')')
                time.sleep(0.1)
            else:
                print('Not changing Block: ' + str(test) + ' (counter = ' + str(counter) + ')')
