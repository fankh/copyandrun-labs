rule Demo_Marker_Script
{
    meta:
        description = "demo marker strings in a script"
    strings:
        $a = "Invoke-DemoPayload" ascii nocase
        $b = "DEMO_STAGE_TWO" ascii
    condition:
        any of them
}

rule Beacon_Config
{
    strings:
        $k = "C2_BEACON_INTERVAL" ascii
        $u = "LabTestAgent" ascii
    condition:
        all of them
}
