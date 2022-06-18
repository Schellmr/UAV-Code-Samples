/*    */ package moe.tendies.autoclicker.hook.device.mouse;
/*    */ 
/*    */ import com.sun.jna.Pointer;
/*    */ import com.sun.jna.platform.win32.User32;
/*    */ import com.sun.jna.platform.win32.WinDef;
/*    */ import moe.tendies.autoclicker.hook.device.DeviceEventReceiver;
/*    */ import moe.tendies.autoclicker.hook.device.mouse.struct.LowLevelMouseProc;
/*    */ import moe.tendies.autoclicker.hook.device.mouse.struct.MSLLHOOKSTRUCT;
/*    */ import moe.tendies.autoclicker.hook.device.mouse.struct.MouseButtonType;
/*    */ 
/*    */ public abstract class MouseEventReceiver
/*    */   extends DeviceEventReceiver<MouseHookManager> implements LowLevelMouseProc {
/*    */   private static final int WM_MOUSELDOWN = 513;
/*    */   private static final int WM_MOUSELUP = 514;
/*    */   private static final int WM_MOUSEMDOWN = 519;
/*    */   
/* 17 */   public MouseEventReceiver(MouseHookManager hookManager) { super(hookManager); }
/*    */   private static final int WM_MOUSEMUP = 520; private static final int WM_MOUSERDOWN = 516;
/*    */   private static final int WM_MOUSERUP = 517;
/*    */   
/*    */   public WinDef.LRESULT callback(int nCode, WinDef.WPARAM wParam, MSLLHOOKSTRUCT info) {
/* 22 */     boolean cancel = false;
/* 23 */     int code = wParam.intValue();
/*    */     
/* 25 */     if (code == 513 || code == 516 || code == 519) {
/* 26 */       cancel = onMousePress(MouseButtonType.fromWParam(code), info);
/* 27 */     } else if (code == 514 || code == 517 || code == 520) {
/* 28 */       cancel = onMouseRelease(MouseButtonType.fromWParam(code), info);
/*    */     } 
/*    */     
/* 31 */     if (cancel) {
/* 32 */       return new WinDef.LRESULT(1L);
/*    */     }
/*    */     
/* 35 */     Pointer ptr = info.getPointer();
/* 36 */     long peer = Pointer.SIZE;
/* 37 */     return User32.INSTANCE.CallNextHookEx(((MouseHookManager)getHookManager()).getHhk(this), nCode, wParam, new WinDef.LPARAM(peer));
/*    */   }
/*    */   
/*    */   public abstract boolean onMousePress(MouseButtonType paramMouseButtonType, MSLLHOOKSTRUCT paramMSLLHOOKSTRUCT);
/*    */   
/*    */   public abstract boolean onMouseRelease(MouseButtonType paramMouseButtonType, MSLLHOOKSTRUCT paramMSLLHOOKSTRUCT);
/*    */ }


/* Location:              C:\Users\Schell\Desktop\autoclicker_2018.06.14.16.29.jar!\re\badwa\autoclicker\hook\device\mouse\MouseEventReceiver.class
 * Java compiler version: 9 (53.0)
 * JD-Core Version:       1.0.7
 */