import mcpi.minecraft as minecraft # Load libraries
from ISStreamer.Streamer import Streamer
import mcpi.block as block
import time, datetime, psutil

for pros in psutil.pids(): # Get the Linux process number for the Minecraft program
    if psutil.Process(pros).name() == 'minecraft-pi' and len(psutil.Process(pros).cmdline()) == 1:
        pm = psutil.Process(pros)
streamer=Streamer(bucket_name=":mushroom: Terraforming", bucket_key="<enter here>", access_key= "<eneter here>")
Free_account = False # If using a free IS account, set to True to limit data uploads & avoid exceeding monthly limit
# Function to Upload various bits of data to IS
def upload_data_to_IS(speed,elapsed,blocks_processed, blocks_transformed,cpu,y,x,z,mem,pm,num_blocks):
    print('Uploading to Initial State')
    streamer.log(":snail: Run Speed",speed)
    streamer.log(":jack_o_lantern: Run2 Time since last "+ str(num_blocks) + "blocks",elapsed)
    streamer.log(":volcano: Run2 Total Blocks",blocks_processed)
    streamer.log(":chocolate_bar:Run2  Blocks transformed",blocks_transformed)
    streamer.log(":up: CPU %",cpu)
    streamer.log(":arrow_down: Y",y)
    streamer.log(":arrow_right: X",x)
    streamer.log(":arrow_left: Z",z)
    streamer.log(":question: Memory used %",mem.percent)
    streamer.log(":question: Minecraft Process memory used %",pm.memory_percent())

time.sleep(1)
mc=minecraft.Minecraft.create() # Connect to Minecraft
keepblocks=[block.AIR.id,block.WATER.id,block.LAVA.id,block.SNOW.id,block.WATER_FLOWING.id,block.WATER_STATIONARY]
counter = 0 # A bunch of variables to keep track of how many blocks have been processed
blocks_processed = 0
blocks_transformed = 0
blocks_since = 0
throttle = 5 # Use this when Free_account is True, to restrict amount of data uploaded
num_blocks = 1000 # How many blocks to transform before pausing to let Minecraft catch-up
start = time.time()
for x in range(-128,128): # the x-direction
    for y in range(-4,35): # the y-direction (up/down)
        for z in range(-128,128): # the z-direction
            print(x,y,z)
            test = mc.getBlock(x,y,z) # Read a block at x,y,z
            blocks_processed+=1
            blocks_since+=1
            if test not in keepblocks: # Don't transform these blocks (should always contain AIR)
                counter+=1
                if counter > num_blocks:
                    blocks_transformed+=num_blocks
                    counter = 0
                    stop = time.time()
                    elapsed = stop - start # How long since last group of blocks were processed?
                    speed = blocks_since/elapsed # calculate speed
                    cpu = psutil.cpu_percent() # Read CPU utilisation
                    mem = psutil.virtual_memory() # read memory usage data
                    if Free_account: # Only bother to throttle if using free IS account
                        if throttle == 0:
                            upload_data_to_IS(speed,elapsed,blocks_processed, blocks_transformed,cpu,y,x,z,mem,pm,num_blocks)
                            throttle = 5
                        else:
                            throttle-=1
                            print('reducing throttle')
                    else:
                        upload_data_to_IS(speed,elapsed,blocks_processed, blocks_transformed,cpu,y,x,z,mem,pm, num_blocks)
                    time.sleep(5) # Pause to allow Minecraft catch-up
                    start = time.time()
                    blocks_since=0
                mc.setBlock(x,y,z,block.REDSTONE_ORE.id) # <- set this: the block to which you want other transformed
                print('Changing Block: ' + str(test) + ' (counter = ' + str(counter) + ')')
                time.sleep(0.1)
            else:
                print('Not changing Block: ' + str(test) + ' (counter = ' + str(counter) + ')')
