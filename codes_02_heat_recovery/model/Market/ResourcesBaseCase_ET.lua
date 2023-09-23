local osmose = require 'osmose'
local et = osmose.Model 'Resources_ET'

et.header = {
  name = '',
  displayName = '',
  authors = {'Daniel Flórez-Orrego, EPFL IPESE research group'},
  developers = {''},
  contributors = {''},
  creation_date = '',
  updates = {''},
  versions = {'1.0'},
  confidentiality = {''},
  title = 'Resources, market and wastes',
  description = [[Resources, market and wastes]],
  references = {''},
  adaptedwith = {},
  notes =  {}
}
--------------------------
--------- Inputs ---------
--------------------------

et.inputs = {
  water_cost = {default = 3.5, unit='Euro/m^3'}, -- price of water https://www.waternewseurope.com/water-prices-compared-in-36-eu-cities/
  CW_ref_VOLF = {default = 1000, unit='m^3/h'}, -- a large provider of water
  elec_cost = {default = 0.2, unit='Euro/kWh'}, -- price of electricity 0.073-0.108 EUR/kWh 
  ELEC_ref_POWER = {default = 1000, unit='kW'}, -- a large provider of electricity
  natgas_cost =  {default = 0.08,unit = 'Euro/kWh'}, -- price of natural gas
  NATGAS_ref_LOAD = {default = 1000, unit='kW'}, -- a large provider of natural gas
  dioxidecapt_cost = {default = 0.0084, unit='Euro/kg'}, -- cost of marketable CO2 (slaughterhouses, beverage industry, etc.)
  CO2capt_ref_LOAD = {default = 1000, unit='kg/h'}, -- a large receiver of CO2 captured
  dioxidetax_cost = {default = 100, unit='Euro/t'}, -- carbon dioxide tax avg. 120 Eur/tCO2 emitted
  CO2taxed_ref_LOAD = {default = 1000, unit='kg/h'}, -- a large receiver of CO2 emitted
  ammo_cost =  {default = 0.098,unit = 'Euro/kWh'}, -- avg. 32 USD/GJ ECOS 2016 Florez-Orrego LHV 18.6 MJ/kg
  AMMO_ref_LOAD = {default = 1000, unit='kW'}, -- a large receiver of ammonia
  biomsw_cost = {default = 0.001, unit='Eur/t'}, -- assumed cost of digestable organic fraction of MSW
  BIOMSW_ref_LOAD = {default = 1000, unit='t/h'}, -- a large provider of biomass organic fraction of metropolitan solid wastes
  biowood_cost = {default = 0.014, unit='Eur/kWh'}, -- cost of woody biomass for gasification or combustion
  BIOWOOD_ref_LOAD = {default = 1000, unit='kW'}, -- a large provider of external of woody biomass for gasification or combustion
  I_CO2fuel = {default = 2.75, unit='kgCO2/kgCh4'}, -- methane direct CO2 emission factor
  r_CO2fuel = {default = 0.0049, unit='gCO2/kJCH4'}, -- methane indirect CO2 emission factor (Florez-Orrego 2015)
  r_CO2ee = {default = 62.63, unit='gCO2/kWh'}, -- electricity indirect CO2 emission factor 62gCO2/kWh (Florez-Orrego 2015)
  r_CO2biowood = {default = 0.0039, unit='gCO2/kJbiowood'}, -- biowood indirect CO2 emission factor (Florez-Orrego 2015)
  LHV_NG = {default = 50000, unit='kJ/kg'}, -- lower heating value of methane
  LHV_BioWood = {default = 11328, unit = 'kJ/kg'}, -- wet woody bimoass 40% moisture, if dry biomass 18879 kJ/kg

  -- Specific brewery costs
  beer_cost = {default = 10000, unit='Eur/m3'}, -- price of beer 5 Eur per 1 pint (500 mL) = 5 Eur/0.5 L = 10000 Eur/m3 https://www.swissinfo.ch/eng/business/pricey-pilsner_beer-in-geneva-is-most-expensive-in-world/41521290
  BEER_ref_VOLF = {default = 1000, unit='m^3/h'}, -- a large receiver of beer
  husk_cost = {default = 0.003, unit='Eur/kg'}, -- assume 1% of the malt
  HUSK_ref_LOAD = {default = 1000, unit='kg/h'}, -- a large receiver of spent grain waste
  malt_cost = {default = 0.307, unit='Euro/kg'}, -- price of malt 307 Eur/t = 0.33 Eur/kg https://agriculture.ec.europa.eu/data-and-analysis/markets/overviews/market-observatories/crops/cereals-statistics_en and https://www.inside.beer/news/detail/germany-breweries-face-huge-malt-price-hike-in-october/ and https://www.tridge.com/intelligences/barley-malt/price
  MALT_ref_LOAD = {default = 1000, unit='kg/h'}, -- a large provider of malt
  soda_cost = {default = 0.3, unit='Euro/kg'}, -- price of soda 0.3 Eur/kg https://lca-net.com/files/naoh.pdf
  SODA_ref_LOAD = {default = 1000, unit='kg/h'}, -- a large provider of soda
  corn_cost = {default = 0.317, unit='Euro/kg'}, -- price of corn 317 Eur/t https://agriculture.ec.europa.eu/data-and-analysis/markets/overviews/market-observatories/crops/cereals-statistics_en and https://live.euronext.com/en/product/commodities-futures/EMA-DPAR
  CORN_ref_LOAD  = {default = 1000, unit='kg/h'}, -- a large provider of corn


 }

--------------------------
--------- Outputs ---------
--------------------------

et.outputs = {
  CW_COST = {unit='Euro/h',job='water_cost*CW_ref_VOLF'}, -- Eur/m3 * m3/h
  ELEC_SELL_COST = {unit='Euro/h',job='elec_cost*ELEC_ref_POWER'},
  ELEC_BUY_COST = {unit='Euro/h',job='-1*ELEC_SELL_COST()*0.8'}, -- lower to avoid oversizing and net export
  NATGAS_COST = {unit='Euro/h',job='natgas_cost*NATGAS_ref_LOAD'},
  NATGAS_BUY = {unit='Euro/h',job='-natgas_cost*NATGAS_ref_LOAD*0.8'}, -- 0.8 times lower to avoid oversizing and net export
  CO2_BUY_COST = {unit='Euro/h',job='-1*dioxidecapt_cost*CO2capt_ref_LOAD'}, -- cost of CO2 exported for further applications
  CO2_TAX_COST = {unit='Euro/h',job='dioxidetax_cost/1000*CO2taxed_ref_LOAD'}, -- CO2 for emitting
  CO2_CREDIT_COST = {unit='Euro/h',job='-dioxidetax_cost/1000*CO2taxed_ref_LOAD'}, -- CO2 for injecting
  CO2_INJ_COST = {unit='Euro/h',job='-dioxidetax_cost/1000*CO2capt_ref_LOAD'}, -- cost of CO2 credits for renewable CO2 injection
  AMMO_BUY_COST = {unit='Euro/h',job='-1*ammo_cost*AMMO_ref_LOAD'},
  BIOMSW_SELL_COST = {unit='Euro/h',job='biomsw_cost*BIOMSW_ref_LOAD'}, -- organic fraction of BioMSW
  BIOWOOD_SELL_COST = {unit='Euro/h',job='biowood_cost*BIOWOOD_ref_LOAD'}, -- -- Eur/kWh * kW,
  --DirectEmNG = {unit='kg/h',job='I_CO2fuel*NATGAS_ref_LOAD/LHV_NG*3600'}, --kg/h of CO2
  IndEmittedNG = {unit='kg/h',job='r_CO2fuel*NATGAS_ref_LOAD*3600/1000'}, --kg/h of CO2
  IndEmittedEE = {unit='kg/h',job='r_CO2ee*ELEC_ref_POWER/1000'}, --kg/h of CO2
  IndEmittedWood = {unit='kg/h',job='r_CO2biowood*BIOWOOD_ref_LOAD*3600/1000'}, --kg/h of CO2
  -- Specific brewery costs 
  BEER_BUY_COST = {unit='Euro/h',job='-1*beer_cost*BEER_ref_VOLF'}, -- Eur/m3 * m3/h
  HUSK_BUY_COST = {unit='Euro/h',job='-1*husk_cost*HUSK_ref_LOAD'}, -- Eur/kg * kg/h,
  MALT_SELL_COST = {unit='Euro/h',job='malt_cost*MALT_ref_LOAD'}, -- Eur/kg * kg/h,
  SODA_SELL_COST = {unit='Euro/h',job='soda_cost*SODA_ref_LOAD'}, -- Eur/kg * kg/h,
  CORN_SELL_COST = {unit='Euro/h',job='corn_cost*CORN_ref_LOAD'}, -- Eur/kg * kg/h,

}


--------------------------
--------- Layers ---------
--------------------------

et:addLayers {Elec = {type= 'ResourceBalance', unit = 'kW'} }
et:addLayers {water = {type= 'ResourceBalance', unit = 'm^3/h'} }
et:addLayers {CO2 = {type= 'ResourceBalance', unit = 'kg/h'} } 
et:addLayers {CH4 = {type= 'ResourceBalance', unit = 'kW'} }
et:addLayers {NH3 = {type= 'ResourceBalance', unit = 'kW'}}
et:addLayers {CO2inFlueGas = {type= 'ResourceBalance', unit = 'kg/h'}}  
et:addLayers {CO2inject = {type= 'ResourceBalance', unit = 'kg/h'}}  
et:addLayers {Liq_CO2 = {type ='ResourceBalance', unit ='kg/h'}}
et:addLayers {EnvCO2Em = {type= 'ResourceBalance', unit = 'kg/h'} }
et:addLayers {BioMSW  = {type ='ResourceBalance', unit ='t/h'}}
et:addLayers {BioWood = {type = 'ResourceBalance', unit = 'kW'}}
et:addLayers {Digestate = {type ='ResourceBalance', unit ='kg/h'}}
et:addLayers {BEER = {type ='ResourceBalance', unit ='m3/h'}}
et:addLayers {HUSK = {type ='ResourceBalance', unit ='kg/h'}}
et:addLayers {MALT = {type ='ResourceBalance', unit ='kg/h'}}	
et:addLayers {SODA = {type ='ResourceBalance', unit ='kg/h'}}
et:addLayers {CORN = {type ='ResourceBalance', unit ='kg/h'}}



-- et:addLayers {hydrogen = {type = 'ResourceBalance', unit ='kg/h'}} -- Other layers can be created

--------------------------
--- Units and streams ----
--------------------------

-- Electricity to the process (sold by the grid to the process) -- comenting the electricity and allowing the steam network to generate it, can be obtained more accurate, actual profiles
et:addUnit('ElecFromGrid',{type='Utility', Fmin = 0, Fmax = 100000000, Cost1 = 0, Cost2 = 'ELEC_SELL_COST'})
et['ElecFromGrid']:addStreams{
  elec_sell = rs({'Elec', 'out', 'ELEC_ref_POWER'}),
  indCO2Em_EEgrid = rs({'EnvCO2Em', 'out', 'IndEmittedEE'}) --kg/h per 1000 kW of electricity
}

-- Electricity from the process (bought by the grid to the steam network)
et:addUnit('ElecToGrid',{type='Utility', Fmin = 0, Fmax = 1, Cost1 = 0, Cost2 = 'ELEC_BUY_COST'})
et['ElecToGrid']:addStreams{
 elec_buy = rs({'Elec', 'in', 'ELEC_ref_POWER'}) 
}

-- Water to the process
et:addUnit('WaterFromGrid',{type='Utility', Fmin = 0, Fmax = 1000, Cost1 = 0, Cost2 = 'CW_COST'})
et['WaterFromGrid']:addStreams{
  water_sell = rs({'water', 'out', 'CW_ref_VOLF'})
}

-- Water from the process (methanator can deliver above 350 m3/h of water, that if not used needs to be rejected)
et:addUnit('WaterToGrid',{type='Utility', Fmin = 0, Fmax = 1000, Cost1 = 0, Cost2 = 0})
et['WaterToGrid']:addStreams{
  water_claim = rs({'water', 'in', 'CW_ref_VOLF'})
}



-- Natural Gas furnace and boilers (NO FOSSIL NATGAS WILL BE ALLOWED)
et:addUnit('NatGasFromGrid',{type='Utility', Fmin = 0, Fmax = 1000, Cost1 = 0, Cost2 = 'NATGAS_COST'})
et['NatGasFromGrid']:addStreams{
  natGas_fuel = rs({'CH4', 'out', 'NATGAS_ref_LOAD'}), -- in kW
  indCO2Em_NGgrid = rs({'EnvCO2Em', 'out', 'IndEmittedNG'}) --kg/h direct
}



--[[
-- Natural gas purchase for allowing purchase of SNG by the NG grid
et:addUnit('NatGasToGrid',{type='Utility', Fmin = 0, Fmax = 1000, Cost1 = 0, Cost2 = 'NATGAS_BUY'})
et['NatGasToGrid']:addStreams{
  natGas_fuel = rs({'CH4', 'in', 'NATGAS_ref_LOAD'}),
}
]]


-- External Biomass Marketed for Digestion(organic fraction of solid wastes) 
et:addUnit('BioMSWGrid',{type='Utility', Fmin = 0, Fmax = 10000000, Cost1 = 0, Cost2 = 'BIOMSW_SELL_COST'})
et['BioMSWGrid']:addStreams{
  biomsw_sell = rs({'BioMSW', 'out', 'BIOMSW_ref_LOAD'}), -- t/h
  -- indCO2Em_BioMSW= rs({'EnvCO2Em', 'out', 'IndEmittedBioMSW'}) --kg/h per t/h of BioMSW NOT DEFINED YET
}

-- External Biomass Marketed for Combustion or Gasification (woody biomass) 
et:addUnit('BioWoodGrid',{type='Utility', Fmin = 0, Fmax = 10000000, Cost1 = 0, Cost2 = 'BIOWOOD_SELL_COST'})
et['BioWoodGrid']:addStreams{
  biowood_sell = rs({'BioWood', 'out', 'BIOWOOD_ref_LOAD'}), -- kW
  indCO2Em_BioWood = rs({'EnvCO2Em', 'out', 'IndEmittedWood'}) --kg/h per 1000 kW of biomass
}


-- CO2 fossil emitted in the furnace flue gas (diluted state, taxed)
et:addUnit('FlueGasCO2',{type='Utility', Fmin = 0, Fmax = 10000, Cost1 = 0, Cost2 = 0}) 
et['FlueGasCO2']:addStreams{
  CO2_fluegas = rs({'CO2inFlueGas', 'in', 'CO2taxed_ref_LOAD'}), --kg/h
  CO2_fluegas_Env = rs({'EnvCO2Em', 'out', 'CO2taxed_ref_LOAD'}) --kg/h released to environment
}



-- Pure CO2 vented to atmosphere (excess, taxed)
et:addUnit('CO2PureToEnv',{type='Utility', Fmin = 0, Fmax = 10000, Cost1 = 0, Cost2 = 0}) -- 
et['CO2PureToEnv']:addStreams{
  CO2_pure = rs({'CO2', 'in', 'CO2capt_ref_LOAD'}),  
  CO2_pure_Env = rs({'EnvCO2Em', 'out', 'CO2capt_ref_LOAD'}) --kg/h released to environment
}


--[[
-- Pure CO2 sold to other industries (sold although not taxed, considering further uses)
et:addUnit('CO2PureExport',{type='Utility', Fmin = 0, Fmax = 10000, Cost1 = 0, Cost2 = 'CO2_BUY_COST'}) 
et['CO2PureExport']:addStreams{
  CO2_exported = rs({'Liq_CO2', 'in', 'CO2capt_ref_LOAD'}) --kg/h
}
]]

  -- Pure CO2 injected, assumes there are incentives for injection regardless if it is fossil or biogenic
  et:addUnit('CO2injected',{type='Utility', Fmin = 0, Fmax = 10000, Cost1 = 0, Cost2 = 'CO2_CREDIT_COST'}) -- There should be A CREDIT!!!!
  et['CO2injected']:addStreams{
    CO2_injected = rs({'CO2inject', 'in', 'CO2capt_ref_LOAD'})  
  }

  -- Environmental atmosphere receiving the fossil emissions TAXED
  et:addUnit('Environ',{type='Utility', Fmin = 0, Fmax = 10000000, Cost1 = 0, Cost2 = 'CO2_TAX_COST'}) -- The environment, a large receiver of biogenic taxed CO2
  et['Environ']:addStreams{
    Environ_CO2Em = rs({'EnvCO2Em', 'in', 'CO2taxed_ref_LOAD'}), -- in kg/h
  }

  -- Digestate Disposal
  et:addUnit('Landfill',{type='Utility', Fmin = 0, Fmax = 10000, Cost1 = 0, Cost2 = 0})
  et['Landfill']:addStreams{
    landfill = rs({'Digestate', 'in', 'BIOMSW_ref_LOAD'}) -- t/h
  }

---- Brewery inputs, products and by-products

  -- Beer Marketed
  et:addUnit('BeerGrid',{type='Utility', Fmin = 0, Fmax = 1000, Cost1 = 0, Cost2 = 'BEER_BUY_COST'})
  et['BeerGrid']:addStreams{
    beer_buy = rs({'BEER', 'in', 'BEER_ref_VOLF'}) -- m3/h
  }

  -- Husk Waste Grid
  et:addUnit('HuskWaste',{type='Utility', Fmin = 0, Fmax = 1000, Cost1 = 0, Cost2 = 'HUSK_BUY_COST'})
  et['HuskWaste']:addStreams{
    husk_buy = rs({'HUSK', 'in', 'HUSK_ref_LOAD'}) -- kg/h
  } 

  -- Malt Grid
  et:addUnit('MaltGrid',{type='Utility', Fmin = 0, Fmax = 1000, Cost1 = 0, Cost2 = 'MALT_SELL_COST'})
  et['MaltGrid']:addStreams{
    malt_sell = rs({'MALT', 'out', 'MALT_ref_LOAD'}) -- kg/h
  } 

  -- Soda Grid
  et:addUnit('SodaGrid',{type='Utility', Fmin = 0, Fmax = 1000, Cost1 = 0, Cost2 = 'SODA_SELL_COST'})
  et['SodaGrid']:addStreams{
    soda_sell = rs({'SODA', 'out', 'SODA_ref_LOAD'}) -- kg/h
  } 

  -- Corn Grid
  et:addUnit('CornGrid',{type='Utility', Fmin = 0, Fmax = 1000, Cost1 = 0, Cost2 = 'CORN_SELL_COST'})
  et['CornGrid']:addStreams{
    corn_sell = rs({'CORN', 'out', 'CORN_ref_LOAD'}) -- kg/h
  } 

-- Other providers and receivers can be defined

-- Hydrogen provider
--[[et:addUnit('H2FromGrid',{type='Utility', Fmin = 0, Fmax = 100000, Cost1 = 0, Cost2 = 'H2_SELL_COST'})
  et['H2FromGrid']:addStreams{
    hydrogen_sell = rs({'hydrogen', 'out', 'H2_ref_LOAD'})
}]]

-- Hydrogen receiver
--[[et:addUnit('H2ToGrid',{type='Utility', Fmin = 0, Fmax = 100000, Cost1 = 0, Cost2 = 'H2_BUY_COST'})
  et['H2ToGrid']:addStreams{
    hydrogen_sell = rs({'hydrogen', 'in', 'H2_ref_LOAD'})
}]]

return et