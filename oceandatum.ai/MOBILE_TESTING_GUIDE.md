# Mobile Testing Guide
**Local Testing Setup for Mobile Navigation**

---

## 🚀 Local Server Running

**Status:** ✅ Running on http://localhost:8080
**Port:** 8080
**Process ID:** Check with `netstat -ano | grep 8080`

---

## 📱 Test Pages Available

### 1. Mobile Test Page
**URL:** http://localhost:8080/mobile-test.html

**Purpose:** Isolated testing of tab navigation
**Features:**
- Simulated mobile viewport (375px)
- Three test scenarios (3, 5, and long-text tabs)
- Visual debugging information
- Viewport width display

### 2. Actual CV Page
**URL:** http://localhost:8080/cv.html

**Purpose:** Test real implementation
**Features:**
- Full CV/Bio page
- Bibliography section
- Actual navigation

### 3. Landing Page
**URL:** http://localhost:8080/index.html

**Purpose:** Test main navigation
**Features:**
- Main site navigation
- Social icons
- Dropdown menus

---

## 🔍 How to Test Mobile View

### Method 1: Chrome DevTools (Recommended)

1. **Open page in Chrome:**
   - http://localhost:8080/cv.html

2. **Open DevTools:**
   - Press `F12` or `Ctrl+Shift+I`

3. **Toggle Device Toolbar:**
   - Press `Ctrl+Shift+M`
   - Or click "Toggle device toolbar" icon (phone/tablet icon)

4. **Select Device:**
   - Choose "iPhone SE" (375px width) or
   - Choose "iPhone 12 Pro" (390px width) or
   - Choose "Responsive" and drag to desired width

5. **Test Navigation:**
   - Click on tab buttons
   - Try to scroll left/right on the tab bar
   - Verify all text is visible
   - Check if scrollbar appears

### Method 2: Browser Resize

1. **Open page:** http://localhost:8080/cv.html
2. **Resize browser window** to narrow width (< 768px)
3. **Test tab navigation**

### Method 3: Actual Mobile Device

1. **Find your computer's local IP:**
   ```bash
   ipconfig | grep "IPv4"
   ```

2. **Open on phone:**
   - Connect phone to same WiFi network
   - Visit: http://[YOUR_IP]:8080/cv.html
   - Example: http://192.168.1.100:8080/cv.html

---

## ✅ What to Verify

### Tab Navigation (cv.html)

**Expected Behavior:**
- ✅ All 3 tab buttons visible: "CV", "Biography", "Bibliography"
- ✅ If tabs don't fit, horizontal scrollbar appears
- ✅ Can scroll left/right to access all tabs
- ✅ No text is cut off (no "Bio..." or "Biblio...")
- ✅ Tabs snap into position when scrolling
- ✅ Touch-friendly scrolling on mobile devices

**Current Issue (If Any):**
- ❌ Tabs showing "CV", "Biog...", "Bibli..." (text cut off)
- ❌ No scrollbar visible
- ❌ Cannot access all tabs
- ❌ Tabs wrapping to multiple lines

### Main Navigation (index.html)

**Expected Behavior:**
- ✅ All navigation items accessible
- ✅ "About", "Projects", "Contact", "Login" all visible
- ✅ Horizontal scrolling if needed
- ✅ Social icons visible

**Current Issue (If Any):**
- ❌ Navigation wrapping
- ❌ Items cut off
- ❌ No scrolling available

---

## 🐛 Debugging Checklist

### 1. Check CSS is Applied

Open DevTools → Elements → Select `.tab-nav`:

**Should see:**
```css
.tab-nav {
    overflow-x: auto;                    /* ← CRITICAL */
    -webkit-overflow-scrolling: touch;
    display: flex;
}
```

**Should see on `.tab-button`:**
```css
.tab-button {
    flex: 1 0 auto;       /* ← DON'T SHRINK */
    min-width: 120px;     /* ← MINIMUM WIDTH (desktop) */
    min-width: 100px;     /* ← MINIMUM WIDTH (mobile) */
    white-space: nowrap;  /* ← NO WRAP */
}
```

### 2. Check Mobile Media Query

At < 768px width, should see:

```css
@media (max-width: 768px) {
    .tab-nav {
        scroll-snap-type: x mandatory;
    }
    .tab-button {
        min-width: 100px;
        scroll-snap-align: start;
    }
}
```

### 3. Check Computed Styles

In DevTools → Elements → Computed tab:

- `overflow-x` should be `auto` (not `visible` or `hidden`)
- `min-width` should be `100px` or `120px` (not `0px`)
- `white-space` should be `nowrap` (not `normal`)
- `flex-shrink` should be `0` (not `1`)

---

## 🔧 Common Issues & Fixes

### Issue 1: Tabs Cut Off, No Scrolling

**Symptoms:**
- Text shows "CV", "Bio...", "Bibli..."
- No scrollbar visible
- Cannot scroll left/right

**Diagnosis:**
- Check if `overflow-x: auto` is being overridden
- Check if `min-width` is set correctly
- Check if browser is caching old CSS

**Fix:**
```bash
# Clear browser cache
Ctrl+Shift+Delete → Clear cache

# Hard refresh
Ctrl+F5

# Or in DevTools, check "Disable cache" and refresh
```

### Issue 2: Tabs Wrapping to Multiple Lines

**Symptoms:**
- Tabs stacked vertically
- Multiple rows of buttons

**Diagnosis:**
- `flex-wrap` might be set to `wrap`
- `white-space` not set to `nowrap`

**Fix:**
Ensure in CSS:
```css
.tab-nav {
    flex-wrap: nowrap; /* Add if missing */
}
.tab-button {
    white-space: nowrap; /* Add if missing */
}
```

### Issue 3: Tabs Too Small on Mobile

**Symptoms:**
- Text is readable but buttons too small to tap
- Touch targets < 44px

**Diagnosis:**
- `min-width` too small
- `padding` too small

**Fix:**
```css
.tab-button {
    min-width: 100px;        /* Increase if needed */
    padding: 0.75rem 1rem;   /* Ensure adequate padding */
}
```

---

## 📸 Visual Testing

### Screenshots to Take

1. **Desktop (> 768px):**
   - Full tab navigation
   - All tabs visible side-by-side

2. **Tablet (768px):**
   - Transition point
   - Should show horizontal scroll if needed

3. **Mobile (375px - iPhone SE):**
   - Compact view
   - Horizontal scrolling active
   - Scrollbar visible

4. **Mobile (320px - Small phone):**
   - Smallest supported width
   - Should still be usable

---

## 🎯 Success Criteria

### Mobile Tab Navigation Works When:

- [x] All tab text fully visible (no truncation)
- [x] Can scroll horizontally to access all tabs
- [x] Scrollbar appears when tabs exceed viewport width
- [x] Tabs snap into position when scrolling
- [x] Touch-friendly (easy to tap and scroll)
- [x] Minimum 44px touch target height
- [x] Smooth momentum scrolling on iOS
- [x] Works on Chrome, Safari, Firefox mobile

---

## 🛠️ Live Editing in DevTools

### Test CSS Changes Without Saving

1. Open DevTools → Elements
2. Select `.tab-nav` or `.tab-button`
3. Edit CSS in real-time
4. See changes immediately
5. If fix works, update actual CSS file

### Useful Test Edits:

```css
/* Try increasing min-width */
.tab-button {
    min-width: 130px !important;
}

/* Try forcing overflow */
.tab-nav {
    overflow-x: scroll !important;
}

/* Try different flex settings */
.tab-button {
    flex: 0 0 auto !important;
}
```

---

## 📋 Test Report Template

After testing, record results:

```
## Mobile Navigation Test Results

**Date:** [DATE]
**Browser:** Chrome [VERSION]
**Device:** iPhone SE Simulator / Actual Device
**Viewport:** 375px x 667px

### CV.HTML - Tab Navigation
- [ ] All tabs visible: CV, Biography, Bibliography
- [ ] Horizontal scrolling works
- [ ] Scrollbar appears
- [ ] Snap scrolling works
- [ ] Touch-friendly
- [ ] Issue: [DESCRIBE ANY ISSUES]

### INDEX.HTML - Main Navigation
- [ ] All nav items accessible
- [ ] Horizontal scrolling works
- [ ] Dropdowns work on mobile
- [ ] Issue: [DESCRIBE ANY ISSUES]

### Recommendations:
1. [FIX #1]
2. [FIX #2]
```

---

## 🚦 Next Steps

### If Tests Pass:
1. Stop local server: `Ctrl+C` in server terminal
2. Commit changes with mobile test results
3. Push to GitHub
4. Verify on live site in 1-2 minutes

### If Tests Fail:
1. Document specific issues found
2. Fix CSS based on debugging guide above
3. Re-test locally
4. Repeat until all tests pass
5. Then commit and push

---

## 💡 Additional Resources

### Browser Testing Tools
- Chrome DevTools: F12
- Firefox Developer Tools: F12
- Safari Web Inspector: Cmd+Opt+I

### Mobile Simulators
- Chrome DevTools Device Mode
- Firefox Responsive Design Mode
- BrowserStack (cloud testing)
- Sauce Labs (cloud testing)

### Viewport Sizes to Test
- 320px - Small phone (iPhone SE 1st gen)
- 375px - iPhone SE / iPhone 6/7/8
- 390px - iPhone 12 Pro
- 414px - iPhone 12 Pro Max
- 768px - iPad (breakpoint)

---

**Server URLs for Testing:**
- Main: http://localhost:8080/
- CV: http://localhost:8080/cv.html
- Mobile Test: http://localhost:8080/mobile-test.html
- Index: http://localhost:8080/index.html
- Tampa Cement: http://localhost:8080/projects/tampa-cement.html
