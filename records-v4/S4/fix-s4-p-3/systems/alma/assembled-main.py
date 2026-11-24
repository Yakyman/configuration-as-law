#!/usr/bin/env python3
"""Run the unchanged collector plus the new DNF event field adapter."""
import pathlib,sys
R=pathlib.Path(__file__).resolve().parent
CORE=R.parent/'collector'
sys.path.insert(0,str(R))
sys.path.insert(0,str(CORE))
import main,extended,key_events
original=extended.collect
def collect(ctx):
 original(ctx)
 if ctx.meta['system']=='alma':key_events.collect(ctx)
extended.collect=collect
raise SystemExit(main.main())
