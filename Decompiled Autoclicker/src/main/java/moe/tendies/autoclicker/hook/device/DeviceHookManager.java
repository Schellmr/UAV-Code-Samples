/*    */ package moe.tendies.autoclicker.hook.device;
/*    */ 
/*    */ import com.sun.jna.platform.win32.WinUser;
/*    */ import java.util.HashMap;
/*    */ import java.util.Map;
/*    */ 
/*    */ public abstract class DeviceHookManager<H extends DeviceEventReceiver<?>, T extends DeviceHookThread<?>>
/*    */   extends Object {
/*  9 */   private final Map<H, T> hooks = new HashMap();
/*    */   
/*    */   public void hook(H eventReceiver) {
/* 12 */     T t = (T)createHookThread(eventReceiver);
/* 13 */     this.hooks.put(eventReceiver, t);
/* 14 */     t.start();
/*    */   }
/*    */   
/* 17 */   public void unhook(H eventReceiver) { ((DeviceHookThread)this.hooks.get(eventReceiver)).unhook(); }
/*    */ 
/*    */   
/* 20 */   public WinUser.HHOOK getHhk(H eventReceiver) { return ((DeviceHookThread)this.hooks.get(eventReceiver)).getHHK(); }
/*    */   
/*    */   public abstract T createHookThread(H paramH);
/*    */ }


/* Location:              C:\Users\Schell\Desktop\JUnit_2018.06.14.16.29.jar!\re\badwa\junit\hook\device\DeviceHookManager.class
 * Java compiler version: 9 (53.0)
 * JD-Core Version:       1.0.7
 */