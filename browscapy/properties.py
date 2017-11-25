"""All browscap properties."""
from typing import NamedTuple


class Properties(NamedTuple):  # pylint: disable=too-few-public-methods
    """All properties found in browscap.csv."""

    PropertyName: str
    MasterParent: str
    LiteMode: str
    Parent: str
    Comment: str
    Browser: str
    Browser_Type: str
    Browser_Bits: str
    Browser_Maker: str
    Browser_Modus: str
    Version: str
    MajorVer: str
    MinorVer: str
    Platform: str
    Platform_Version: str
    Platform_Description: str
    Platform_Bits: str
    Platform_Maker: str
    Alpha: str
    Beta: str
    Win16: str
    Win32: str
    Win64: str
    Frames: str
    IFrames: str
    Tables: str
    Cookies: str
    BackgroundSounds: str
    JavaScript: str
    VBScript: str
    JavaApplets: str
    ActiveXControls: str
    isMobileDevice: str
    isTablet: str
    isSyndicationReader: str
    Crawler: str
    isFake: str
    isAnonymized: str
    isModified: str
    CssVersion: str
    AolVersion: str
    Device_Name: str
    Device_Maker: str
    Device_Type: str
    Device_Pointing_Method: str
    Device_Code_Name: str
    Device_Brand_Name: str
    RenderingEngine_Name: str
    RenderingEngine_Version: str
    RenderingEngine_Description: str
    RenderingEngine_Maker: str
