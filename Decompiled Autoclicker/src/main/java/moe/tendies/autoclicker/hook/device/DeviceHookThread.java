/*    */ package moe.tendies.autoclicker.hook.device;
/*    */ import com.sun.jna.platform.win32.Kernel32;
import com.sun.jna.platform.win32.User32;
/*    */ import com.sun.jna.platform.win32.WinDef;
import com.sun.jna.platform.win32.WinUser;
/*    */ 
/*    */ public abstract class DeviceHookThread<H extends DeviceEventReceiver<?>> extends Thread {
/*    */   private final H eventReceiver;
/*    */   private final WinUser.MSG msg;
/*    */   
/*    */   public DeviceHookThread(H eventReceiver, int type) {
/* 10 */     this.msg = new WinUser.MSG();
/*    */ 
/*    */ 
/*    */ 
/*    */     
/* 15 */     this.eventReceiver = eventReceiver;
/* 16 */     this.hookType = type;
/*    */   }
/*    */   private final int hookType; private WinUser.HHOOK hhk;
/*    */   
/*    */   public void run() {
/* 21 */     WinDef.HMODULE handle = Kernel32.INSTANCE.GetModuleHandle(null);
/* 22 */     this.hhk = User32.INSTANCE.SetWindowsHookEx(this.hookType, this.eventReceiver, handle, 0);
/*    */     int result;
/* 24 */     while ((result = getMessage()) != 0) {
/* 25 */       if (result == -1) {
/* 26 */         onFail();
/*    */         break;
/*    */       } 
/* 29 */       dispatchEvent();
/*    */     } 
/*    */     
/* 32 */     unhook();
/*    */   }
/*    */ 
/*    */   
/* 36 */   private int getMessage() { return User32.INSTANCE.GetMessage(this.msg, null, 0, 0); }
/*    */ 
/*    */   
/*    */   private void dispatchEvent() {
/* 40 */     User32.INSTANCE.TranslateMessage(this.msg);
/* 41 */     User32.INSTANCE.DispatchMessage(this.msg);
/*    */   }
/*    */ 
/*    */   
/*    */   protected abstract void onFail();
/*    */   
/* 47 */   public void unhook() { User32.INSTANCE.UnhookWindowsHookEx(this.hhk); }
/*    */ 
/*    */ 
/*    */   
/* 51 */   public WinUser.HHOOK getHHK() { return this.hhk; }
/*    */ }


/* Location:              C:\Users\Schell\Desktop\JUnit_2018.06.14.16.29.jar!\re\badwa\junit\hook\device\DeviceHookThread.class
 * Java compiler version: 9 (53.0)
 * JD-Core Version:       1.0.7
 */