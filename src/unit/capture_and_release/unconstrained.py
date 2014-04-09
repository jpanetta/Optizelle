# This tests our ability to capture and release from the optimization state

#---Import0---
import Optizelle 

import Optizelle.Unconstrained.State
import Optizelle.Unconstrained.Functions
import Optizelle.Unconstrained.Algorithms
import Optizelle.Unconstrained.Restart
import Optizelle.json.Unconstrained
#---Import1---

import numpy
import math

# Create some type shortcuts
XX = Optizelle.Rm
msg = Optizelle.Messaging()
    
# Create some arbitrary vector in R^2
x = numpy.array([1.2,2.3])
x0 = numpy.array([2.3,1.2])

# Create an unconstrained state based on this vector
state=Optizelle.Unconstrained.State.t(XX,msg,x)

# Read and write the state to file
fname = "restart.json"
#---WriteReadRestart0---
Optizelle.json.Unconstrained.write_restart(
    XX,msg,fname,state);
Optizelle.json.Unconstrained.read_restart(
    XX,msg,fname,x,state);
#---WriteReadRestart1---

# Do a release 
#---Release0---
xs = Optizelle.Unconstrained.Restart.X_Vectors()
reals = Optizelle.Unconstrained.Restart.Reals()
nats = Optizelle.Unconstrained.Restart.Naturals()
params = Optizelle.Unconstrained.Restart.Params()
Optizelle.Unconstrained.Restart.release(
    XX,msg,state,xs,reals,nats,params)
#---Release1---

# Check that we have the correct number of vectors
if len(xs) != 6:
    msg.error("The list xs contains the wrong number of vectors.")

# Modify some vectors 
xs[0]=(xs[0][0],x0)

# Capture the state
#---Capture0---
Optizelle.Unconstrained.Restart.capture(
    XX,msg,state,xs,reals,nats,params)
#---Capture1---

# Check the relative error between the vector created above and the one
# left in the state
residual = XX.init(x)
XX.copy(x0,residual)
XX.axpy(-1.,state.x,residual)
err=(math.sqrt(XX.innr(residual,residual))
    /(1+math.sqrt(XX.innr(x0,x0))))

if err >= 1e-15:
    msg.error("Too much error in the captured x")
