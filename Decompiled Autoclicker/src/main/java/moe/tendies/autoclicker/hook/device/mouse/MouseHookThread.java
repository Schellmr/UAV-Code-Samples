/*    */ package moe.tendies.autoclicker.hook.device.mouse;
/*    */ 
/*    */ import moe.tendies.autoclicker.hook.device.DeviceHookThread;
/*    */ 
/*    */ public class MouseHookThread
/*    */   extends DeviceHookThread<MouseEventReceiver>
/*    */ {
/*  8 */   public MouseHookThread(MouseEventReceiver eventReceiver) { super(eventReceiver, 14); }
/*    */ 
/*    */ 
/*    */ 
/*    */   
/* 13 */   public void onFail() { System.err.println("Invalid message result for mouse hook, aborting"); }
/*    */ }


/* Location:              C:\Users\Schell\Desktop\JUnit_2018.06.14.16.29.jar!\re\badwa\junit\hook\device\mouse\MouseHookThread.class
 * Java compiler version: 9 (53.0)
 * JD-Core Version:       1.0.7
 */