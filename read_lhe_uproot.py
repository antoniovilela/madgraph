import uproot
import awkward as ak
import numpy as np
import pandas as pd

def read_lhe_uproot( rootFileName ):
    
    root_ = uproot.open( rootFileName )
    
    tree_ = root_[ "LHEF" ]
    print ( tree_.keys() )
    
    keys_events_ = [ 'Event/Event.Number',
         'Event/Event.Nparticles',
         'Event/Event.ProcessID',
         'Event/Event.Weight',
         'Event/Event.ScalePDF',
         'Event/Event.CouplingQED',
         'Event/Event.CouplingQCD' ]
    events_ = tree_.arrays( keys_events_, library="ak", how="zip" )
    events_ = events_[ 'Event/Event' ]
    
    print ( "Number of events: {}".format( len( events_ ) ) )
    
    keys_particles_ = [ 'Particle/Particle.PID',
         'Particle/Particle.Status',
         'Particle/Particle.Mother1',
         'Particle/Particle.Mother2',
         'Particle/Particle.ColorLine1',
         'Particle/Particle.ColorLine2',
         'Particle/Particle.Px',
         'Particle/Particle.Py',
         'Particle/Particle.Pz',
         'Particle/Particle.E',
         'Particle/Particle.M',
         'Particle/Particle.PT',
         'Particle/Particle.Eta',
         'Particle/Particle.Phi',
         'Particle/Particle.Rapidity',
         'Particle/Particle.LifeTime',
         'Particle/Particle.Spin' ]
    particles_ = tree_.arrays( keys_particles_, library="ak", how="zip" )
    particles_ = particles_[ 'Particle/Particle' ]
    particles_[ "event" ] = events_[ 'Number' ][:,0]
    
    df_ = pd.DataFrame( np.array( ak.flatten( particles_ ) ) ).set_index( ['event'], drop=False )
    
    return df_