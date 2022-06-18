package moe.tendies.autoclicker.hook.device.mouse.struct;

import com.sun.jna.platform.win32.WinDef;
import com.sun.jna.platform.win32.WinUser;

public interface LowLevelMouseProc extends WinUser.HOOKPROC {
  WinDef.LRESULT callback(int paramInt, WinDef.WPARAM paramWPARAM, MSLLHOOKSTRUCT paramMSLLHOOKSTRUCT);
}


/* Location:              C:\Users\Schell\Desktop\JUnit_2018.06.14.16.29.jar!\re\badwa\junit\hook\device\mouse\struct\LowLevelMouseProc.class
 * Java compiler version: 9 (53.0)
 * JD-Core Version:       1.0.7
 */