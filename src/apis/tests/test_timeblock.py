from .. import models

# Create your tests here.

# Test1 init
def test_timeblock_init():
    timeBlock = models.TimeBlock(
        label="A",
        M_start_time="1:00",
        M_end_time="2:00",
        T_start_time="3:00",
        T_end_time="4:00",
        W_start_time="5:00",
        W_end_time="6:00",
        H_start_time="7:00",
        H_end_time="8:00",
        F_start_time="9:00",
        F_end_time="10:00"
    )
    assert timeBlock.label == "A"
    assert timeBlock.days == {
        "M": {"start": "1:00", "end": "2:00"},
        "T": {"start": "3:00", "end": "4:00"},
        "W": {"start": "5:00", "end": "6:00"},
        "H": {"start": "7:00", "end": "8:00"},
        "F": {"start": "9:00", "end": "10:00"}
    }

# Test2 changeTime
def test_changeTime():
    timeBlock = models.TimeBlock(
        label="A",
        M_start_time="1:00",
        M_end_time="2:00",
        T_start_time="3:00",
        T_end_time="4:00",
        W_start_time="5:00",
        W_end_time="6:00",
        H_start_time="7:00",
        H_end_time="8:00",
        F_start_time="9:00",
        F_end_time="10:00"
    )
    timeBlock.changeTime(day= "H", new_start= "17:00", new_end= "18:00")
    assert timeBlock.days == {
        "M": {"start": "1:00", "end": "2:00"},
        "T": {"start": "3:00", "end": "4:00"},
        "W": {"start": "5:00", "end": "6:00"},
        "H": {"start": "17:00", "end": "18:00"},
        "F": {"start": "9:00", "end": "10:00"}
    }
    timeBlock.changeTime(day= "H")
    assert timeBlock.days == {
        "M": {"start": "1:00", "end": "2:00"},
        "T": {"start": "3:00", "end": "4:00"},
        "W": {"start": "5:00", "end": "6:00"},
        "H": None,
        "F": {"start": "9:00", "end": "10:00"}
    }


# Test3 getOutputDict
def test_getOutputDict():
    timeBlock = models.TimeBlock(
        label="A",
        M_start_time="1:00",
        M_end_time="2:00",
        T_start_time="3:00",
        T_end_time="4:00",
        W_start_time="5:00",
        W_end_time="6:00",
        H_start_time="7:00",
        H_end_time="8:00",
        F_start_time=None,
        F_end_time=None
    )
    result = timeBlock.getOutputDict()
    assert result == {
        "M": {"start": "1:00", "end": "2:00"},
        "T": {"start": "3:00", "end": "4:00"},
        "W": {"start": "5:00", "end": "6:00"},
        "H": {"start": "7:00", "end": "8:00"},
    }

# Test4 getLabel
def test_getLabel():
    timeBlock = models.TimeBlock(
        label="A",
        M_start_time="1:00",
        M_end_time="2:00",
        T_start_time="3:00",
        T_end_time="4:00",
        W_start_time="5:00",
        W_end_time="6:00",
        H_start_time="7:00",
        H_end_time="8:00",
        F_start_time=None,
        F_end_time=None
    )
    result = timeBlock.getLabel()
    assert result == "A"

# Test5 getBlock
def test_getBlock():
    timeBlockLists = [
        models.TimeBlock("A"),
        models.TimeBlock("B"),
        models.TimeBlock("C")
    ]
    result = models.getBlock(timeBlockLists, "A")
    assert result.getLabel() == "A"
    result = models.getBlock(timeBlockLists, "N")
    assert result == -1
