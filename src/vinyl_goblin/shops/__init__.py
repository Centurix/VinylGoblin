from .rockaway_records import RockawayRecords
from .rocking_horse_records import RockingHorseRecords
from .stash_records import StashRecords
from .record_exchange import RecordExchange
from .dutch_vinyl import DutchVinyl
from .catalog_music import CatalogMusic
from .monster_robot import MonsterRobot
from .glitter_records import GlitterRecords
from .sonic_sherpa import SonicSherpa
from .relove_oxley import ReloveOxley
from .blackened_records import BlackenedRecords
from .jet_black_cat_records import JetBlackCatRecords
from .waxx_lyrical import WaxxLyricalRecords
from .spin_and_groove_records import SpinAndGrooveRecords
from .hideous_records import HideousRecords


shops = [
    RockingHorseRecords,
    StashRecords,
    RockawayRecords,
    RecordExchange,
    DutchVinyl,
    CatalogMusic,
    MonsterRobot,
    GlitterRecords,
    SonicSherpa,
    ReloveOxley,
    BlackenedRecords,
    JetBlackCatRecords,
    WaxxLyricalRecords,
    SpinAndGrooveRecords,
    HideousRecords,
]

__all__ = [
    "shops"
]
