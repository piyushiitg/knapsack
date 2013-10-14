#// Input:
#// Values (stored in array v)
#// Weights (stored in array w)
#// Number of distinct items (n)
#// Knapsack capacity (W)
#for w from 0 to W do
#  m[0, w] := 0
#end for 
#for i from 1 to n do
#  for j from 0 to W do
#    if j >= w[i] then
#      m[i, j] := max(m[i-1, j], m[i-1, j-w[i]] + v[i])
#    else
#      m[i, j] := m[i-1, j]
#    end if
#  end for
#end for
from sys import stdin
class Session:
     def __init__(self,starttime,endtime):
         self.starttime = starttime*60
         self.endtime =  endtime*60
         self.talks = []

     def addtalks(self,talk):
         self.talks.append(talk)

     #Print all  then talks related to the session 
     def print_talks(self):
           cur_time = self.starttime
           for talk in self.talks:
               t = formattime(cur_time)
               print t, talk[0],talk[1]
               cur_time += talk[1]
     # calculate the end time of the session for networking event starttime          
     def talk_end_time(self):
           tsum = 0
           for i in self.talks:
               tsum = tsum + i[1]
           tsum = tsum + self.starttime
           return tsum
  
class Track:
    def __init__(self):
        self.morning = None
        self.afternoon = None
    
    def newsession(self,type):
         if type=="morning":
             self.morning = Session(9,12)
             return self.morning
         else:
             self.afternoon = Session(13,17)
             return self.afternoon
         
    def print_talks(self):
        if self.morning:
            self.morning.print_talks()
            print "12:00PM Lunch 60"
       
        if self.afternoon:
            self.afternoon.print_talks()
            t = self.afternoon.talk_end_time()        
            if t > 960:
                t = formattime(t)    
            else:
                t = "4:00PM"
            print t, "Networking Event"

class Scheduler:
    def __init__(self):
        self.inputlist = read_input()
        # add one dummy variable to run the matrixx loop from 1 
        self.inputlist.insert(0,("dummy",0))
        self.tracks = []  
    #remove those conference whose time is greater then 240
    def senitizeinput(self):
        r = []
        for talk in self.inputlist:
            if talk[1] > 240: 
                r.append(talk)
        for r1 in r:
            self.inputlist.remove(r1)
    
    def run(self):
        while len(self.inputlist) > 1:
            t = Track()
            self.tracks.append(t)
            mtalks = self.schedule(t,"morning")
            self.delete_from_input(mtalks)
            if self.inputlist:
                atalks = self.schedule(t,"afternoon")
                self.delete_from_input(atalks)
    
    def delete_from_input(self,mtalks):
        for m in mtalks:
            self.inputlist.remove(m)
                     
    def schedule(self,track,type):
        session = track.newsession(type)
        a = self.conference_scheduler(session)
        for a1 in a:
            session.addtalks(a1)
        return a
    # Similer to 0/1 Knapsack problem and that is solved using dynamic programming   
    def conference_scheduler(self,session):
        weights = self.inputlist
        values = weights
        nitems = len(weights)
        #mknap is a matrix that will have a all posible for given set
        mknap = []
        #xdirect is the array to find out real values
        xdirect = []
        SIZE = session.endtime - session.starttime
        for i in range(nitems+1):
            mknap.append([0]*(SIZE+1))
            xdirect.append([0]*(SIZE+1))
        for i in range(SIZE+1):
            mknap[0][i] = 0
            xdirect[0][i] = 0

        time = session.starttime
        
        for i in range(1,nitems):
            for j in range(0,SIZE+1):
                if j >= weights[i][1]:
                    # max of if you reject ith value and if you select ith value
                    mknap[i][j] = max(mknap[i-1][j], mknap[i-1][j-weights[i][1]] + values[i][1])
                    if mknap[i-1][j] > mknap[i-1][j-weights[i][1]] + values[i][1]:
                        xdirect[i][j] = j
                    else:
                        xdirect[i][j] = j - weights[i][1]
                else:
                    mknap[i][j] = mknap[i-1][j]
                    xdirect[i][j] = j

        selected = []
        i = nitems-1
        j = SIZE
        while j>0 and i>0:
            if xdirect[i][j] != j:
                t = formattime(time)
                selected.append(weights[i])
                time = time + weights[i][1]
                j = xdirect[i][j]
            i = i -1
        return selected
    

    def print_schedule(self):
        for tno,track in enumerate(self.tracks):
	    print "Track:",tno+1
	    track.print_talks()
            print ""

#read the input from command line
def read_input():
    lines = []
    for line in stdin.readlines():
        rindex = line.rfind(" ")
        talk = line[0:rindex]
        time = line[rindex+1:]
        if "lightning" in time:
            time = "5"
        else:
            time = time.replace("min", "")
        time = int(time.strip())
        lines.append((talk,time))
    return lines

# format the time in AM and PM format
def formattime(time):
    hour = time/60
    if (hour < 12):
        dtime = "AM" 
    else:
        dtime = "PM"
    if (hour > 12):
        hour = (hour-12) 
    return "%02d:%02d%s"% (hour, (time % 60), dtime)
 
if __name__ == '__main__':
    print "Please start typing----> talkname duration"
    s = Scheduler()
    s.senitizeinput()    
    s.run()
    s.print_schedule()
