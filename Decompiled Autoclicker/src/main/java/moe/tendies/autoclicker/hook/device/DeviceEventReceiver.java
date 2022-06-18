/*    */ package moe.tendies.autoclicker.hook.device;
/*    */ 
/*    */ import com.sun.jna.platform.win32.WinUser;
/*    */ 
/*    */ public class DeviceEventReceiver<D extends DeviceHookManager<?, ?>>
/*    */   extends Object implements WinUser.HOOKPROC {
/*    */   private final D hookManager;
/*    */   
/*  9 */   public DeviceEventReceiver(D hookManager) { this.hookManager = hookManager; }
/*    */ 
/*    */ 
/*    */   
/* 13 */   protected final D getHookManager() { return (D)this.hookManager; }
/*    */ }


/* Location:              C:\Users\Schell\Desktop\JUnit_2018.06.14.16.29.jar!\re\badwa\junit\hook\device\DeviceEventReceiver.class
 * Java compiler version: 9 (53.0)
 * JD-Core Version:       1.0.7
 */