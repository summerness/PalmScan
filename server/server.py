from settings.setting import API_IMG_PATH
import os
from models.models import *
from core.feature.color import color
from core.roi.roi import ROI
from core.contour import contour as cont
from core.feature.thenar.feature import ThenarFeature
from core.feature.roi_5.feature import Roi5Feature
from core.feature.small_thenar.feature import SmallThenarFeature



class BackServer(object):
    @classmethod
    def upload_image(cls, file_info, open_id):
        file_name = file_info['filename']
        path = os.path.join(API_IMG_PATH, open_id)
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
        try:
            session = DBSession()
            save_path = os.path.join(path, file_name)
            with open(save_path, 'wb') as f:
                f.write(file_info['body'])
            p = PInfo(
                open_id=open_id,
                img_path=save_path,
                img_name=file_name,
                img_full_path=path,
            )
            session.add(p)
            session.commit()
            return "success"
        except Exception as e:
            return "failed"

    @classmethod
    def image_handle(cls, openid):
        session = DBSession()
        info = session.query(PInfo).filter_by(open_id=openid).first()
        image_path = info.img_path
        img_name = info.img_name
        full_path = info.full_path
        c = cont.Contour(
            img_name,
            image_path,
            full_path
        )

        ## 未作异常处理，后期优化，别忘记了

        c.cutSkin()
        ct, skin, contour, contourSkin = c.drawContour()

        r = ROI(contour, skin, contourSkin)
        r.roi(ct, img_name, full_path)
        roi_main = r.roi_main(ct)
        roi_thenar = r.roi_thenar()
        roi_small_thenar = r.roi_small_thenar()
        roi_5 = r.roi_5()
        roi_7 = r.roi_7()
        co = color.ColorFeature(roi_main)
        v_color = co.GetColor()

        ##Thenar
        t = ThenarFeature(roi_thenar, full_path, img_name)
        t.pre_image()
        cross_count = t.draw_cross()

        ##SThenar
        st = SmallThenarFeature(roi_small_thenar, full_path, img_name)
        scount = st.pre_image()


        ##ROI5
        r5  = Roi5Feature(roi_5, full_path, img_name)
        r5.pre_image()
        r5.fix_line()
        is_r5_exist = r5.getLenAndDraw()

        ##