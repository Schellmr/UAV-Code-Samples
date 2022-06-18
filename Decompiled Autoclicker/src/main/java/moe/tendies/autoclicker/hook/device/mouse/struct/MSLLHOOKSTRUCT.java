/*    */ package moe.tendies.autoclicker.hook.device.mouse.struct;
/*    */ 
/*    */ import com.sun.jna.Structure;
/*    */ import com.sun.jna.platform.win32.BaseTSD;
/*    */ import com.sun.jna.platform.win32.WinDef;
/*    */ import java.util.Arrays;
/*    */ import java.util.List;
/*    */ 
/*    */ 
/*    */ public class MSLLHOOKSTRUCT
/*    */   extends Structure
/*    */ {
/*    */   public WinDef.POINT pt;
/*    */   public WinDef.DWORD mouseData;
/*    */   public WinDef.DWORD flags;
/*    */   public WinDef.DWORD time;
/*    */   public BaseTSD.ULONG_PTR dwExtraInfo;
/*    */   
/* 19 */   protected List<String> getFieldOrder() { return Arrays.asList(new String[] { "pt", "mouseData", "flags", "time", "dwExtraInfo" }); }
/*    */ }


/* Location:              C:\Users\Schell\Desktop\JUnit_2018.06.14.16.29.jar!\re\badwa\junit\hook\device\mouse\struct\MSLLHOOKSTRUCT.class
 * Java compiler version: 9 (53.0)
 * JD-Core Version:       1.0.7
 */