import os
import shutil
import json

# CLEAR ANY PREVIOUS BUILD DATA
os.system("rm -rf temp dist && mkdir dist")

os.system("git clone https://github.com/BetterLectio/betterLectio.git temp")

transfers = {
    "./items/svelte.config.js": "./temp/svelte.config.js",
    "./items/jsconfig.json": "./temp/jsconfig.json",
    "./items/build.config.json": "./temp/build.config.json",

    "./items/electron.cjs": "./temp/src/electron.cjs",
    "./items/preload.cjs": "./temp/src/preload.cjs",
}

print()

for originalLocation, newLocation in transfers.items():
    print(f"Transferring {originalLocation} into {newLocation}")
    shutil.copyfile(originalLocation, newLocation)

# MODIFYING PACKAGE.JSON
package = json.loads(open("temp/package.json").read())
package["dependencies"]["electron-window-state"] = "^5.0.3"
package["dependencies"]["electron-context-menu"] = "^3.6.1"
package["dependencies"]["electron-serve"] = "^1.1.0"
package["dependencies"]["electron-reloader"] = "^1.2.3"
package["dependencies"]["discord-rpc"] = "^4.0.1"
package["dependencies"]["@popperjs/core"] = "^2.11.6"
package["dependencies"]["open"] = "^8.4.0"
package["dependencies"]["moment"] = "^2.29.4"

package["devDependencies"]["electron"] = "^22.0.3"
package["devDependencies"]["electron-builder"] = "^24.0.0"
package["devDependencies"]["concurrently"] = "^7.6.0"
package["devDependencies"]["@sveltejs/adapter-static"] = "^1.0.5"
package["devDependencies"]["svelte-preprocess"] = "^4.10.7"
package["devDependencies"]["cross-env"] = "^7.0.3"
package["devDependencies"]["node-wget"] = "^0.4.3"
package["devDependencies"]["del-cli"] = "^5.0.0"

package["main"] = "src/electron.cjs"
package["author"] = "Better Lectio Team"
package["description"] = "Better Lectio er en forbedring af Lectio, et dansk lektionssystem. Vi har gjort det nemmere at finde informationer og få overblik over skolegangen. Vi har også lavet en ny, brugervenlig og moderne brugerflade. Better Lectio er open source, så alle kan se koden og bidrage. Projektet er stadig under udvikling, så hvis du har forslag eller finder fejl, er du velkommen til at åbne en issue på GitHub."

package["scripts"]["build-electron-linux"] = "concurrently --maxProcesses=1 \"cross-env NODE_ENV=production BUILD_TYPE=app vite build\" \"electron-builder -l --config build.config.json\""
#package["scripts"]["build-backend"] = "concurrently --maxProcesses=1 \"del static/backend/*\" \"wget https://raw.githubusercontent.com/BetterLectio/BetterLectio-Flask-Backend/main/api/app.py -d static/backend/backend.py\" \"wget https://raw.githubusercontent.com/BetterLectio/BetterLectio-Flask-Backend/main/requirements.txt -d static/backend/\" \"pip install -r static/backend/requirements.txt\" \"pip install pyinstaller\" \"pyinstaller --onefile static/backend/backend.py --distpath static/backend/ --workpath temp/\" \"del temp backend.spec static/backend/requirements.txt\""

open("temp/package.json", "w").write(json.dumps(package, indent=2))

# REMOVING MIXPANEL
layout = open("temp/src/routes/+layout.js").read()
layout = layout.replace("""import { PUBLIC_MIXPANEL_TOKEN } from "$env/static/public";
import mixpanel from 'mixpanel-browser';

mixpanel.init(PUBLIC_MIXPANEL_TOKEN, {
  host: "api-eu.mixpanel.com",
  debug: true,
});
mixpanel.set_config({ 'persistence': 'localStorage' })""", "")
open("temp/src/routes/+layout.js", "w").write(layout)

PageTransition = open("temp/src/lib/components/PageTransition.svelte").read()
PageTransition = PageTransition.replace('import mixpanel from "mixpanel-browser";', "")
PageTransition = PageTransition.replace("""  $: if (previous && end) {
    mixpanel.track(`on ${pathname}`, { page: pathname });
    if (end - start > 100) {
      console.log(`%c Route change (${pathname}) in ${end - start}ms`, "color: Yellow; font-weight: bold");
    } else {
      console.log(`%c Route change (${pathname}) in ${end - start}ms`, "color: Lightgreen; font-weight: bold");
    }
  }""", "")
open("temp/src/lib/components/PageTransition.svelte", "w").write(PageTransition)

print("\nBeginning build")

# LINUX BUILD
# Building backend - Linux
for command in [
    "rm -rf temp/static/backend",
    "wget https://raw.githubusercontent.com/BetterLectio/BetterLectio-Flask-Backend/main/requirements.txt -P temp/static/backend/",
    "wget https://raw.githubusercontent.com/BetterLectio/BetterLectio-Flask-Backend/main/api/app.py -P temp/static/backend -O temp/static/backend/backend.py",
    "pip install -r temp/static/backend/requirements.txt",
    "pip install pyinstaller",
    "pyinstaller --onefile temp/static/backend/backend.py --distpath temp/static/backend/ --workpath temp/temp/",
    "rm -rf temp/temp temp/static/backend/requirements.txt temp/static/backend/backend.py backend.spec"
]:
    os.system(command)

os.system("cd temp && npm install && npm run build-electron-linux")

# WINDOWS BUILD - WINE

# MAC OS BUILD - DARLING


# COPY FILES
shutil.copyfile(f"./temp/dist/{package['name']}-{package['version']}.zip", "./dist/betterlectio-linux.zip")
os.system("rm -rf temp")