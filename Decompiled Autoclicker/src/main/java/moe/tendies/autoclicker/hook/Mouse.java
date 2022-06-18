/*    */ package moe.tendies.autoclicker.hook;
/*    */ 
/*    */ import com.sun.jna.platform.win32.BaseTSD;
/*    */ import com.sun.jna.platform.win32.User32;
/*    */ import com.sun.jna.platform.win32.WinDef;
/*    */ import com.sun.jna.platform.win32.WinUser;
/*    */ 
/*    */ public class Mouse {
/*    */   public static void mouseAction(int x, int y, int flags) {
/* 10 */     WinUser.INPUT input = new WinUser.INPUT();
/*    */     
/* 12 */     input.type = new WinDef.DWORD(0L);
/* 13 */     input.input.setType("mi");
/* 14 */     if (x != -1) {
/* 15 */       input.input.mi.dx = new WinDef.LONG(x);
/*    */     }
/* 17 */     if (y != -1) {
/* 18 */       input.input.mi.dy = new WinDef.LONG(y);
/*    */     }
/* 20 */     input.input.mi.time = new WinDef.DWORD(0L);
/* 21 */     input.input.mi.dwExtraInfo = new BaseTSD.ULONG_PTR(0L);
/* 22 */     input.input.mi.dwFlags = new WinDef.DWORD(flags);
/* 23 */     User32.INSTANCE.SendInput(new WinDef.DWORD(1L), new WinUser.INPUT[] { input }, input.size());
/*    */   }
/*    */ }


/* Location:              C:\Users\Schell\Desktop\JUnit_2018.06.14.16.29.jar!\re\badwa\junit\hook\Mouse.class
 * Java compiler version: 9 (53.0)
 * JD-Core Version:       1.0.7
 */