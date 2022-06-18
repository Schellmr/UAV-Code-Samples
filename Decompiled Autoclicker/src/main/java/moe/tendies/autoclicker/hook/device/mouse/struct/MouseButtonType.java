/*    */ package moe.tendies.autoclicker.hook.device.mouse.struct;
/*    */ 
/*    */ import java.util.HashMap;
/*    */ import java.util.Map;
/*    */ 
/*    */ public enum MouseButtonType {
/*  7 */   LEFT_DOWN(513), LEFT_UP(514),
/*  8 */   RIGHT_DOWN(516), RIGHT_UP(517),
/*  9 */   MIDDLE_DOWN(519), MIDDLE_UP(520);
/*    */   
/*    */   private static Map<Integer, MouseButtonType> types;
/*    */   
/* 13 */   MouseButtonType(int value) { register(value, this); }
/*    */ 
/*    */   
/*    */   private void register(int value, MouseButtonType type) {
/* 17 */     if (types == null) {
/* 18 */       types = new HashMap();
/*    */     }
/* 20 */     types.put(Integer.valueOf(value), type);
/*    */   }
/*    */ 
/*    */   
/* 24 */   public static MouseButtonType fromWParam(int value) { return (MouseButtonType)types.get(Integer.valueOf(value)); }
/*    */ }


/* Location:              C:\Users\Schell\Desktop\JUnit_2018.06.14.16.29.jar!\re\badwa\junit\hook\device\mouse\struct\MouseButtonType.class
 * Java compiler version: 9 (53.0)
 * JD-Core Version:       1.0.7
 */