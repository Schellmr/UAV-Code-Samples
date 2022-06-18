/*   */ package moe.tendies.autoclicker.hook.device.mouse;
/*   */ 
/*   */ import moe.tendies.autoclicker.hook.device.DeviceEventReceiver;
/*   */ import moe.tendies.autoclicker.hook.device.DeviceHookManager;
/*   */ import moe.tendies.autoclicker.hook.device.DeviceHookThread;
/*   */ 
/*   */ public class MouseHookManager extends DeviceHookManager<MouseEventReceiver, MouseHookThread> {
/* 8 */   public MouseHookThread createHookThread(MouseEventReceiver eventReceiver) { return new MouseHookThread(eventReceiver); }
/*   */ }


/* Location:              C:\Users\Schell\Desktop\JUnit_2018.06.14.16.29.jar!\re\badwa\junit\hook\device\mouse\MouseHookManager.class
 * Java compiler version: 9 (53.0)
 * JD-Core Version:       1.0.7
 */